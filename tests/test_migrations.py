import sys, unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
import studio_git

class Migrations(unittest.TestCase):
    def test_approval_is_required_before_any_access(self):
        with patch.object(studio_git,'workspace') as workspace:
            with self.assertRaises(ValueError): studio_git.migrate('migration-apply','folder','app')
            workspace.assert_not_called()
    def test_unsynced_and_local_migrations_are_blocked(self):
        git=Mock();git.text.return_value='head'
        with patch.object(studio_git,'workspace',return_value=(Path('/tmp'),{},git)),patch.object(studio_git,'fetch',return_value='head'),patch.object(studio_git,'changed_paths',return_value=['supabase/migrations/new.sql']),patch.object(studio_git,'operation') as operation:
            with self.assertRaises(ValueError): studio_git.migrate('migration-preview','folder','app')
            operation.assert_not_called();git.close.assert_called_once()
    def test_preview_uses_studio_not_direct_supabase(self):
        git=Mock();git.text.return_value='head'
        with patch.object(studio_git,'workspace',return_value=(Path('/tmp'),{},git)),patch.object(studio_git,'fetch',return_value='head'),patch.object(studio_git,'changed_paths',return_value=[]),patch.object(studio_git,'operation',return_value={'commit':'head','status':'review_required'}) as operation:
            self.assertEqual(studio_git.migrate('migration-preview','folder','app')['status'],'review_required')
            operation.assert_called_once_with('app','migration_preview');git.close.assert_called_once()

if __name__=='__main__': unittest.main()
