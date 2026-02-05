"""
Results Visualization Script
Generates comparison charts for baseline vs AutoPrompt performance
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_results(baseline_path="results/baseline_results.json", 
                 autoprompt_path="results/autoprompt_results.json",
                 report_path="results/benchmark_report.json"):
    """Load results from JSON files"""
    try:
        with open(report_path, 'r') as f:
            report = json.load(f)
        return report
    except FileNotFoundError:
        print(f"Error: Results files not found. Please run main.py first.")
        return None

def create_comparison_chart(report, output_path="results/comparison_chart.png"):
    """Create bar chart comparing baseline vs autoprompt"""
    
    metrics = ['overall_accuracy', 'product_accuracy', 'sentiment_accuracy', 
               'edge_case_accuracy']
    metric_labels = ['Overall\nAccuracy', 'Product\nAccuracy', 
                     'Sentiment\nAccuracy', 'Edge Case\nAccuracy']
    
    baseline_scores = [report['baseline'][m] for m in metrics]
    autoprompt_scores = [report['autoprompt'][m] for m in metrics]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - width/2, baseline_scores, width, label='Baseline', 
                   color='#94a3b8', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, autoprompt_scores, width, label='AutoPrompt', 
                   color='#3b82f6', edgecolor='black', linewidth=1.2)
    
    # Add value labels on bars
    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    autolabel(bars1)
    autolabel(bars2)
    
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Baseline vs AutoPrompt Performance Comparison', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, fontsize=11)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Comparison chart saved to {output_path}")
    
def create_improvement_chart(report, output_path="results/improvement_chart.png"):
    """Create chart showing improvement percentages"""
    
    metrics = ['overall_accuracy', 'product_accuracy', 'sentiment_accuracy', 
               'edge_case_accuracy']
    metric_labels = ['Overall', 'Product', 'Sentiment', 'Edge Cases']
    
    improvements = [report['improvement'][m] for m in metrics]
    colors = ['#10b981' if x > 0 else '#ef4444' for x in improvements]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(metric_labels, improvements, color=colors, 
                   edgecolor='black', linewidth=1.2)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, improvements)):
        ax.text(val + (1 if val > 0 else -1), i, f'{val:+.1f}%',
               va='center', ha='left' if val > 0 else 'right',
               fontweight='bold', fontsize=11)
    
    ax.set_xlabel('Improvement (%)', fontsize=12, fontweight='bold')
    ax.set_title('AutoPrompt Performance Gains', fontsize=14, 
                 fontweight='bold', pad=20)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Improvement chart saved to {output_path}")

def create_summary_metrics(report, output_path="results/summary_metrics.png"):
    """Create a summary metrics visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Overall Accuracy
    categories = ['Baseline', 'AutoPrompt']
    values = [report['baseline']['overall_accuracy'], 
              report['autoprompt']['overall_accuracy']]
    ax1.bar(categories, values, color=['#94a3b8', '#3b82f6'], 
            edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Accuracy (%)', fontweight='bold')
    ax1.set_title('Overall Accuracy', fontweight='bold', fontsize=12)
    ax1.set_ylim(0, 100)
    for i, v in enumerate(values):
        ax1.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Failure Rate
    failure_values = [report['baseline']['failure_rate'], 
                     report['autoprompt']['failure_rate']]
    ax2.bar(categories, failure_values, color=['#f87171', '#fbbf24'],
            edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('Failure Rate (%)', fontweight='bold')
    ax2.set_title('Failure Rate (Lower is Better)', fontweight='bold', fontsize=12)
    for i, v in enumerate(failure_values):
        ax2.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Confidence
    conf_values = [report['baseline']['avg_confidence'], 
                   report['autoprompt']['avg_confidence']]
    ax3.bar(categories, conf_values, color=['#94a3b8', '#3b82f6'],
            edgecolor='black', linewidth=1.2)
    ax3.set_ylabel('Average Confidence', fontweight='bold')
    ax3.set_title('Model Confidence', fontweight='bold', fontsize=12)
    ax3.set_ylim(0, 1)
    for i, v in enumerate(conf_values):
        ax3.text(i, v + 0.03, f'{v:.2f}', ha='center', fontweight='bold')
    
    # Edge Case Performance
    edge_values = [report['baseline']['edge_case_accuracy'], 
                   report['autoprompt']['edge_case_accuracy']]
    ax4.bar(categories, edge_values, color=['#94a3b8', '#3b82f6'],
            edgecolor='black', linewidth=1.2)
    ax4.set_ylabel('Accuracy (%)', fontweight='bold')
    ax4.set_title('Edge Case Handling', fontweight='bold', fontsize=12)
    ax4.set_ylim(0, 100)
    for i, v in enumerate(edge_values):
        ax4.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.suptitle('AutoPrompt Benchmark Summary', fontsize=16, 
                 fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Summary metrics saved to {output_path}")

def main():
    # Ensure results directory exists
    Path("results").mkdir(exist_ok=True)
    
    # Load results
    report = load_results()
    if not report:
        print("\n⚠️  No results found. Run 'python main.py' first to generate benchmark data.")
        return
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    create_comparison_chart(report)
    create_improvement_chart(report)
    create_summary_metrics(report)
    
    print("\n✅ All visualizations created successfully!")
    print("\nGenerated files:")
    print("  - results/comparison_chart.png")
    print("  - results/improvement_chart.png")
    print("  - results/summary_metrics.png")

if __name__ == "__main__":
    main()
