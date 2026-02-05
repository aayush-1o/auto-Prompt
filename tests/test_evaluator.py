"""
Unit tests for evaluator module
"""
import pytest
from src.evaluator import Evaluator
from src.utils import ExtractedData
import tempfile
import json
from pathlib import Path

class TestEvaluator:
    @pytest.fixture
    def sample_ground_truth(self):
        """Create sample ground truth data"""
        data = [
            {
                "review_id": "1",
                "product": "coffee maker",
                "sentiment": "positive",
                "reason": "works great"
            },
            {
                "review_id": "2",
                "product": "blender",
                "sentiment": "negative",
                "reason": "broke quickly"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            temp_path = f.name
        
        yield temp_path
        Path(temp_path).unlink()
    
    @pytest.fixture
    def sample_results(self):
        """Create sample extraction results"""
        return [
            ExtractedData(
                review_id="1",
                product="coffee maker",
                sentiment="positive",
                reason="works great",
                confidence=0.95,
                prompt_used="test"
            ),
            ExtractedData(
                review_id="2",
                product="blender",
                sentiment="negative",
                reason="broke quickly",
                confidence=0.90,
                prompt_used="test"
            )
        ]
    
    def test_evaluator_initialization(self, sample_ground_truth):
        """Test evaluator initialization"""
        evaluator = Evaluator(sample_ground_truth)
        assert len(evaluator.ground_truth) == 2
    
    def test_calculate_metrics_perfect_score(self, sample_ground_truth, sample_results):
        """Test metrics calculation with perfect predictions"""
        evaluator = Evaluator(sample_ground_truth)
        metrics = evaluator.calculate_metrics(sample_results)
        
        assert metrics['overall_accuracy'] == 100.0
        assert metrics['product_accuracy'] == 100.0
        assert metrics['sentiment_accuracy'] == 100.0
        assert metrics['failure_rate'] == 0.0
    
    def test_calculate_metrics_with_errors(self, sample_ground_truth):
        """Test metrics with some errors"""
        evaluator = Evaluator(sample_ground_truth)
        
        results = [
            ExtractedData(
                review_id="1",
                product="coffee",  # Partial match
                sentiment="positive",
                reason="good",
                confidence=0.8,
                prompt_used="test"
            ),
            ExtractedData(
                review_id="2",
                product="error",  # Error case
                sentiment="error",
                reason="failed",
                confidence=0.0,
                prompt_used="test"
            )
        ]
        
        metrics = evaluator.calculate_metrics(results)
        assert metrics['overall_accuracy'] < 100.0
        assert metrics['failure_rate'] > 0.0
    
    def test_generate_report(self, sample_ground_truth, sample_results):
        """Test report generation"""
        evaluator = Evaluator(sample_ground_truth)
        report = evaluator.generate_report(sample_results, sample_results)
        
        assert 'baseline' in report
        assert 'autoprompt' in report
        assert 'improvement' in report
