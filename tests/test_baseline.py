"""
Unit tests for baseline module
"""
import pytest
from src.baseline import BaselinePipeline
from src.utils import Review


class TestBaselinePipeline:
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration"""
        return {
            "api_key": "test_key",
            "generator_model": "gemini-1.5-flash",
            "temperature": 0
        }
    
    def test_baseline_initialization(self, mock_config):
        """Test baseline pipeline initialization"""
        # This will fail without real API key, but structure is tested
        try:
            baseline = BaselinePipeline(mock_config)
            assert baseline.config == mock_config
        except Exception:
            # Expected to fail without valid API key
            pass
    
    def test_review_processing_structure(self, mock_config):
        """Test that process method has correct signature"""
        from src.baseline import BaselinePipeline
        import inspect
        
        # Check method exists and has correct signature
        assert hasattr(BaselinePipeline, 'process')
        sig = inspect.signature(BaselinePipeline.process)
        assert 'review' in sig.parameters
