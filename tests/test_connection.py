import json
from pathlib import Path
import sys
import urllib.parse
from io import StringIO
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import studio_git as module


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.saved = {'app-a': json.dumps({'access_token': 'test-only'}),
                      'app-b': 'other-app'}
        self.store = MagicMock()
        self.store.get_password.side_effect = lambda service, app: self.saved.get(app)
        self.store.delete_password.side_effect = lambda service, app: self.saved.pop(app)
        self.revocation = patch.object(module, 'post', return_value={'revoked': True})
        self.post = self.revocation.start()
        self.addCleanup(self.revocation.stop)
        self.access = patch.object(module, 'access', return_value='test-only-access')
        self.access.start()
        self.addCleanup(self.access.stop)

    def test_disconnect_removes_only_selected_app_and_can_repeat(self):
        with patch.object(module, 'keyring_store', return_value=self.store):
            result = module.disconnect('app-a')
            module.disconnect('app-a')
        self.assertEqual(result['status'], 'disconnected')
        self.assertTrue(result['server_revoked'])
        self.post.assert_called_once_with('mcp-oauth/revoke', {}, 'test-only-access')
        self.assertEqual(self.saved, {'app-b': 'other-app'})
        self.store.delete_password.assert_called_once_with(module.SERVICE, 'app-a')

    def test_connect_clears_old_tokens_before_starting_browser_authorization(self):
        def unavailable_callback(*args):
            self.assertNotIn('app-a', self.saved)
            raise ValueError('Callback unavailable')
        with patch.object(module, 'keyring_store', return_value=self.store), \
                patch.object(module, 'HTTPServer', side_effect=unavailable_callback):
            with self.assertRaisesRegex(ValueError, 'Callback unavailable'):
                module.connect('app-a')
        self.assertNotIn('app-a', self.saved)
        self.assertIn('app-b', self.saved)

    def test_store_failure_prevents_new_authorization(self):
        self.store.delete_password.side_effect = RuntimeError('Store unavailable')
        with patch.object(module, 'keyring_store', return_value=self.store), \
                patch.object(module, 'HTTPServer') as callback:
            with self.assertRaises(RuntimeError):
                module.connect('app-a')
        callback.assert_not_called()

    def test_revocation_failure_clears_local_tokens_and_reports_incomplete_disconnect(self):
        self.post.side_effect = OSError('offline')
        with patch.object(module, 'keyring_store', return_value=self.store):
            with self.assertRaisesRegex(ValueError, 'revocation could not be verified'):
                module.disconnect('app-a')
        self.assertNotIn('app-a', self.saved)

    def test_shared_authorization_is_reused_for_another_app(self):
        self.access.stop()
        self.saved[module.ACCOUNT] = json.dumps({'access_token': 'shared-test-only', 'expires_at': 9999999999})
        with patch.object(module, 'keyring_store', return_value=self.store):
            module.operation('app-b', 'config')
        self.post.assert_called_once_with('local-git', {'project_id': 'app-b', 'action': 'config'}, 'shared-test-only')

    def test_status_without_shared_authorization_never_starts_sign_in(self):
        with patch.object(module, 'keyring_store', return_value=self.store), patch.object(module, 'connect') as connect:
            self.assertEqual(module.connection_status()['connected'], False)
        connect.assert_not_called()
        self.post.assert_not_called()

    def test_mcp_call_returns_only_structured_data_and_uses_shared_auth(self):
        self.post.return_value = {'result': {'structuredContent': {'connected': True, 'roles': ['client']}}}
        result = module.mcp_call('get_connection_status', {})
        self.assertEqual(result, {'connected': True, 'roles': ['client']})
        self.post.assert_called_once_with('mcp', {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
            'params': {'name': 'get_connection_status', 'arguments': {}}}, 'test-only-access')

    def test_connect_can_start_before_an_app_is_selected(self):
        with patch.object(module.sys, 'argv', ['studio_git.py', 'connect']), \
                patch.object(module, 'ensure_helper_runtime'), patch.object(module, 'connect', return_value={'status': 'connected'}) as connect:
            self.assertEqual(module.main(), 0)
        connect.assert_called_once_with(None)

    def test_one_browser_approval_provisions_shared_auth_and_verifies_connection(self):
        self.access.stop()
        self.store.set_password.side_effect = lambda service, key, value: self.saved.__setitem__(key, value)
        opened = []
        server = MagicMock()
        server.__enter__.return_value = server
        server.server_port = 49152
        def callback_server(address, callback):
            def receive():
                state = urllib.parse.parse_qs(urllib.parse.urlparse(opened[0]).query)['state'][0]
                handler = MagicMock()
                handler.path = '/callback?' + urllib.parse.urlencode({'state': state, 'code': 'test-code'})
                callback.do_GET(handler)
            server.handle_request.side_effect = receive
            return server
        def service(path, body, token=None):
            if path == 'mcp-oauth/register':
                return {'client_id': 'test-client'}
            if path == 'mcp-oauth/token':
                return {'access_token': 'test-access', 'refresh_token': 'test-refresh', 'expires_in': 3600}
            return {'result': {'structuredContent': {'connected': True, 'roles': ['client'],
                'granted_scopes': ['projects:read', 'local:write']}}}
        self.post.side_effect = service
        with patch.object(module, 'keyring_store', return_value=self.store), \
                patch.object(module, 'HTTPServer', side_effect=callback_server), \
                patch.object(module.webbrowser, 'open', side_effect=opened.append), \
                patch.object(module.sys, 'stdout', new_callable=StringIO):
            result = module.connect()
        self.assertTrue(result['connected'])
        self.assertEqual(len(opened), 1)
        self.assertEqual([call.args[0] for call in self.post.call_args_list],
            ['mcp-oauth/register', 'mcp-oauth/token', 'mcp'])
        self.assertEqual(self.post.call_args_list[0].args[1]['scope'], 'projects:read local:write')
        self.assertIn(module.ACCOUNT, self.saved)


if __name__ == '__main__':
    unittest.main()
