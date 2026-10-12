import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import hashlib
import json

spec = importlib.util.spec_from_file_location('sync', Path(__file__).parents[1] / 'scripts/sync_workspace.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class SyncTests(unittest.TestCase):
    def test_exclusions_and_changed_files(self):
        hashes={'src/a.ts':'new','.env':'secret','node_modules/a':'x'}
        files=sync.changes({'src/a.ts':'old','src/gone.ts':'old'},hashes,{'src/a.ts':'hello'})
        self.assertEqual(files,[{'path':'src/a.ts','content':'hello'},{'path':'src/gone.ts','content':None}])
    def test_secret_and_binary_changes_stop_before_queueing(self):
        for text in [None, 'api_key="'+'x'*20+'"']:
            with self.assertRaises(ValueError):
                sync.changes({}, {'src/a.ts':'new'}, {'src/a.ts':text})
    def test_supabase_management_tokens_are_blocked(self):
        with self.assertRaises(ValueError):
            sync.changes({}, {'src/config.ts':'new'}, {'src/config.ts':'sbp_'+'a'*40})
    def test_snapshot_excludes_local_metadata_and_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'a.ts').write_text('hello')
            (root/'.studio').mkdir()
            (root/'.studio/token').write_text('not uploaded')
            self.assertEqual(set(sync.snapshot(root)[0]),{'a.ts'})
            (root/'linked.ts').symlink_to(root/'a.ts')
            with self.assertRaises(ValueError):sync.snapshot(root)
    def test_pending_checkpoint_is_persisted_without_grant(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'state.json'
            state={'pending':{'request_id':'stable','files':[{'path':'a','content':'hello'}]}}
            sync.write_state(path,state)
            self.assertNotIn('token',path.read_text())
            self.assertIn('stable',path.read_text())
    def test_credentials_never_sent_to_other_endpoint(self):
        with self.assertRaises(ValueError):sync.request({'endpoint':'https://evil.test','token':'secret'}, {})
    def test_watcher_retries_persisted_checkpoint_and_acknowledges_only_confirmed_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            metadata=root/'.studio'
            metadata.mkdir()
            (root/'a.ts').write_text('changed')
            (metadata/'workspace.json').write_text(json.dumps({'source_commit':'a'*40,'project_id':'app',
                'baseline_file_sha256':{'a.ts':hashlib.sha256(b'original').hexdigest()}}))
            grant={'workspace_id':'workspace','source_commit':'a'*40,'project_id':'app','token':'must-never-save'}
            sent=[]
            def offline(_grant, body):
                sent.append(body.copy())
                raise urllib.error.URLError('offline')
            with patch.object(sync,'request',offline),patch.object(sync.time,'sleep',side_effect=KeyboardInterrupt),patch('builtins.print'):
                with self.assertRaises(KeyboardInterrupt):sync.run(root,grant,quiet=0)
            pending=json.loads((metadata/'sync-state.json').read_text())['pending']
            self.assertEqual(sent[0],pending)
            def online(_grant, body):
                if body['action']=='checkpoint':
                    self.assertEqual(body,pending)
                    return {'state':'queued'}
                return {'job':{'id':pending['request_id'],'state':'done','target_commit':'b'*40,
                    'commit_url':'https://github.com/example/app/commit/'+'b'*40}}
            with patch.object(sync,'request',online),patch.object(sync.time,'sleep',side_effect=KeyboardInterrupt),patch('builtins.print') as output:
                with self.assertRaises(KeyboardInterrupt):sync.run(root,grant,quiet=0)
                self.assertIn('saved_to_studio',output.call_args.args[0])
            state=(metadata/'sync-state.json').read_text()
            self.assertNotIn(grant['token'],state)
            self.assertIsNone(json.loads(state)['pending'])
            self.assertEqual(json.loads(state)['head'],'b'*40)

if __name__=='__main__':unittest.main()
