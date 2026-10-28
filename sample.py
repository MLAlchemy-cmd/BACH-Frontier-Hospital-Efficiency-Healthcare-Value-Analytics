"""
Competition Visualizations - Safety Net Hospital Analysis
Creates three key charts:
1. Waterfall chart (revenue shock impact)
2. Scatter plot (cost vs quality with frontier)
3. Hero vs Struggler comparison bar chart
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle

# Set style for professional looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# STEP 1: Load Your Data
# ============================================================================
# Replace this path with your actual data file path
df = pd.read_csv('merged_healthcare_data.csv')

print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================================================
# HELPER FUNCTIONS (from your notebook)
# ============================================================================

def prepare_condition_data(data, condition, year, min_cases=25):
    """Prepare data for a specific condition and year"""
    # Filter for the year
    d = data[data['year'] == year].copy()
    
    # Get condition-specific columns
    mort_col = f"{condition}_mort_rate"
    readm_col = f"{condition}_readm_rate"
    cases_col = f"{condition}_mort_npatients"
    
    # Filter for minimum cases
    if cases_col in d.columns:
        d = d[d[cases_col] >= min_cases].copy()
    
    # Create safety_net indicator (Medicaid share >= 18%)
    if 'medicaid_share' in d.columns:
        d['safety_net'] = (d['medicaid_share'] >= 0.18).astype(int)
    
    # Calculate quality metrics
    if mort_col in d.columns and readm_col in d.columns:
        d['survival'] = 1 - d[mort_col]
        d['success'] = 1 - d[readm_col]
        d['cases'] = d[cases_col] if cases_col in d.columns else 0
    
    # Select key columns
    keep_cols = ['prov_num', 'year', 'safety_net', 'medicaid_share', 
                 'opexp', 'hours_nursing', 'beds_total_wtd', 
                 'cases', 'survival', 'success']
    
    d = d[[c for c in keep_cols if c in d.columns]].dropna()
    
    return d

# ============================================================================
# VISUALIZATION 1: WATERFALL CHART (Revenue Shock Impact)
# ============================================================================

def create_waterfall_chart(shock_data, save_path='waterfall_hr1_impact.png'):
    """
    Create waterfall chart showing HR 1 revenue impact
    
    Parameters:
    -----------
    shock_data : DataFrame with columns: prov_num, year, income, rev_loss, 
                 net_savings, income_shocked_opt
    """
    
    # Pick the hospital with largest revenue loss
    ex = shock_data.sort_values("rev_loss", ascending=False).head(1).iloc[0]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data for waterfall
    labels = ["Baseline\nIncome", "Revenue Loss\n(HR 1)", "Net Savings\n(Optimization)", 
              "Post-Optimization\nIncome"]
    
    values = [
        ex["income"],
        -ex["rev_loss"],
        ex["net_savings"],
        ex["income_shocked_opt"]
    ]
    
    # Colors
    colors = ['#2ecc71', '#e74c3c', '#3498db', '#2ecc71' if values[-1] > 0 else '#e74c3c']
    
    # Calculate positions
    running = 0
    x_pos = np.arange(len(labels))
    
    # Draw bars
    for i in range(len(labels)-1):
        ax.bar(i, abs(values[i]), bottom=running if values[i] > 0 else running + values[i],
               color=colors[i], alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        if values[i] > 0:
            label_y = running + values[i]/2
        else:
            label_y = running + values[i]/2
        
        ax.text(i, label_y, f'${values[i]/1e6:.1f}M', 
                ha='center', va='center', fontweight='bold', fontsize=10)
        
        running += values[i]
    
    # Final bar (total height)
    ax.bar(len(labels)-1, abs(values[-1]), color=colors[-1], alpha=0.8, 
           edgecolor='black', linewidth=1.5)
    ax.text(len(labels)-1, values[-1]/2, f'${values[-1]/1e6:.1f}M',
            ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Draw connecting lines
    for i in range(len(labels)-1):
        next_y = sum(values[:i+2]) if i < len(labels)-2 else values[-1]
        ax.plot([i+0.4, i+0.6], [sum(values[:i+1]), sum(values[:i+1])], 
                'k--', linewidth=1, alpha=0.5)
    
    # Formatting
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
    ax.set_ylabel('Dollars (Millions)', fontsize=12, fontweight='bold')
    ax.set_title(f'HR 1 Revenue Shock Analysis\nProvider {int(ex["prov_num"])}, Year {int(ex["year"])}',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2)
    
    # Add grid
    ax.grid(axis='y', alpha=0.3)
    
    # Format y-axis to millions
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Waterfall chart saved to {save_path}")
    
    return fig, ax

# ============================================================================
# VISUALIZATION 2: SCATTER PLOT (Cost vs Quality with Frontier)
# ============================================================================

def create_frontier_scatter(efficiency_data, condition='ami', year=2017, 
                           save_path='frontier_scatter.png'):
    """
    Create scatter plot of cost vs quality with efficiency frontier
    
    Parameters:
    -----------
    efficiency_data : DataFrame with columns: opexp, cases, survival, success,
                      medicaid_share, efficiency, on_frontier
    """
    
    # Calculate cost per case
    efficiency_data['cost_per_case'] = efficiency_data['opexp'] / efficiency_data['cases']
    
    # Calculate composite quality score (average of survival and success)
    efficiency_data['quality_score'] = (efficiency_data['survival'] + efficiency_data['success']) / 2
    
    # Remove outliers for better visualization
    q99_cost = efficiency_data['cost_per_case'].quantile(0.99)
    plot_data = efficiency_data[efficiency_data['cost_per_case'] < q99_cost].copy()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Scatter plot - color by Medicaid share
    scatter = ax.scatter(plot_data['quality_score'], 
                        plot_data['cost_per_case'],
                        c=plot_data['medicaid_share'],
                        s=50,
                        alpha=0.6,
                        cmap='RdYlGn_r',  # Red = high Medicaid, Green = low
                        edgecolors='black',
                        linewidth=0.5)
    
    # Highlight frontier hospitals
    frontier = plot_data[plot_data['on_frontier'] == 1]
    ax.scatter(frontier['quality_score'],
              frontier['cost_per_case'],
              s=200,
              marker='*',
              color='gold',
              edgecolors='black',
              linewidth=2,
              label='Frontier Hospitals',
              zorder=5)
    
    # Draw frontier line (approximate with LOWESS or polynomial fit)
    from scipy.interpolate import make_interp_spline
    
    if len(frontier) > 3:
        frontier_sorted = frontier.sort_values('quality_score')
        
        # Smooth frontier line
        x_smooth = np.linspace(frontier_sorted['quality_score'].min(), 
                              frontier_sorted['quality_score'].max(), 100)
        
        # Use polynomial fit (degree 2)
        z = np.polyfit(frontier_sorted['quality_score'], 
                      frontier_sorted['cost_per_case'], 2)
        p = np.poly1d(z)
        
        ax.plot(x_smooth, p(x_smooth), 'r--', linewidth=3, 
               label='Efficiency Frontier', zorder=4)
    
    # Formatting
    ax.set_xlabel('Quality Score (Avg of Survival & Success Rates)', 
                  fontsize=12, fontweight='bold')
    ax.set_ylabel('Cost per Case ($)', fontsize=12, fontweight='bold')
    ax.set_title(f'Hospital Efficiency Frontier: {condition.upper()} ({year})\n' + 
                 'Cost vs. Quality Trade-off',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Medicaid Patient Share', fontsize=11, fontweight='bold')
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    # Grid
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Frontier scatter plot saved to {save_path}")
    
    return fig, ax

# ============================================================================
# VISUALIZATION 3: HERO vs STRUGGLER COMPARISON BAR CHART
# ============================================================================

def create_hero_struggler_comparison(hero_data, save_path='hero_struggler_comparison.png'):
    """
    Create side-by-side bar chart comparing heroes vs strugglers
    
    Parameters:
    -----------
    hero_data : DataFrame with columns: group, admin_share, nurse_intensity,
                occupancy, log_beds, margin
    """
    
    # Calculate group means
    comparison = hero_data.groupby('group')[
        ['admin_share', 'nurse_intensity', 'occupancy', 'log_beds', 'margin']
    ].mean()
    
    # Ensure we have hero and struggler
    if 'hero' not in comparison.index or 'struggler' not in comparison.index:
        print("Warning: Need both 'hero' and 'struggler' groups in data")
        return None, None
    
    # Convert log_beds back to actual bed count
    comparison['beds'] = np.exp(comparison['log_beds'])
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    metrics = [
        ('beds', 'Average Bed Count', 'beds'),
        ('occupancy', 'Occupancy Rate', 'percent'),
        ('admin_share', 'Admin Cost Share', 'percent'),
        ('nurse_intensity', 'Nursing Hours per Bed', 'hours'),
        ('margin', 'Operating Margin', 'percent')
    ]
    
    groups = ['hero', 'struggler']
    colors = ['#2ecc71', '#e74c3c']  # Green for heroes, red for strugglers
    
    for idx, (metric, title, unit) in enumerate(metrics):
        ax = axes[idx]
        
        values = [comparison.loc['hero', metric], comparison.loc['struggler', metric]]
        
        bars = ax.bar(groups, values, color=colors, alpha=0.8, 
                     edgecolor='black', linewidth=2)
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, values)):
            height = bar.get_height()
            
            if unit == 'percent':
                label_text = f'{val*100:.1f}%'
            elif unit == 'beds':
                label_text = f'{val:.0f}'
            else:
                label_text = f'{val:.1f}'
            
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   label_text,
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Formatting
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel(unit.capitalize(), fontsize=10)
        ax.set_xticklabels(['Hero\nHospitals', 'Struggler\nHospitals'], 
                          fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Format y-axis
        if unit == 'percent':
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.0f}%'))
    
    # Remove extra subplot
    fig.delaxes(axes[5])
    
    # Add overall title
    fig.suptitle('Hero vs. Struggler Safety-Net Hospitals: Key Operational Metrics',
                fontsize=16, fontweight='bold', y=0.98)
    
    # Add summary text
    hero_beds = comparison.loc['hero', 'beds']
    strug_beds = comparison.loc['struggler', 'beds']
    size_ratio = strug_beds / hero_beds
    
    summary_text = (f"Key Finding: Struggler hospitals are {size_ratio:.1f}x larger than heroes\n"
                   f"({strug_beds:.0f} vs {hero_beds:.0f} beds on average)")
    
    fig.text(0.65, 0.28, summary_text, 
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Hero vs Struggler comparison saved to {save_path}")
    
    return fig, axes

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("CREATING COMPETITION VISUALIZATIONS")
    print("="*70)
    
    # ------------------------------------------------------------------------
    # 1. PREPARE DATA (you'll need to run your DEA analysis first)
    # ------------------------------------------------------------------------
    
    print("\n1. Preparing data for visualizations...")
    
    # Assuming you have these DataFrames from your analysis:
    # - shock: DataFrame with revenue shock simulation results
    # - eff_df: DataFrame with efficiency scores
    # - sn_reg: DataFrame with hero/struggler classifications
    
    # If you haven't run the full analysis yet, you'll need to:
    # a) Run DEA analysis to get efficiency scores
    # b) Run regression analysis 
    # c) Classify heroes vs strugglers
    # d) Simulate revenue shock
    
    # ------------------------------------------------------------------------
    # 2. CREATE WATERFALL CHART
    # ------------------------------------------------------------------------
    
    print("\n2. Creating waterfall chart...")
    
    # Example of creating shock data if you don't have it yet:
    # This is pseudocode - replace with your actual shock simulation
    """
    shock = pd.DataFrame({
        'prov_num': [...],
        'year': [...],
        'income': [...],  # Baseline operating income
        'rev_loss': [...],  # Revenue loss from HR 1
        'net_savings': [...],  # Savings from optimization
        'income_shocked_opt': [...]  # Final income after shock + optimization
    })
    
    create_waterfall_chart(shock, save_path='waterfall_hr1_impact.png')
    """
    
    # ------------------------------------------------------------------------
    # 3. CREATE FRONTIER SCATTER PLOT
    # ------------------------------------------------------------------------
    
    print("\n3. Creating frontier scatter plot...")
    
    # Example using AMI 2017 data:
    """
    ami2017 = prepare_condition_data(df, 'ami', 2017, min_cases=25)
    
    # Add efficiency scores (you need to run DEA first)
    # Merge with your efficiency results
    # ami2017 = ami2017.merge(eff_df, on=['prov_num', 'year'])
    
    create_frontier_scatter(ami2017, condition='ami', year=2017,
                           save_path='frontier_scatter.png')
    """
    
    # ------------------------------------------------------------------------
    # 4. CREATE HERO VS STRUGGLER COMPARISON
    # ------------------------------------------------------------------------
    
    print("\n4. Creating hero vs struggler comparison...")
    
    # Example with your regression data:
    """
    # sn_reg should have columns: group, admin_share, nurse_intensity, 
    #                             occupancy, log_beds, margin
    
    create_hero_struggler_comparison(sn_reg, 
                                    save_path='hero_struggler_comparison.png')
    """
    
    print("\n" + "="*70)
    print("VISUALIZATION CREATION COMPLETE")
    print("="*70)
    print("\nGenerated files:")
    print("  1. waterfall_hr1_impact.png")
    print("  2. frontier_scatter.png")
    print("  3. hero_struggler_comparison.png")
    print("\nThese visualizations are ready for your competition presentation!")


# ============================================================================
# QUICK TEST WITH SAMPLE DATA
# ============================================================================

def create_sample_visualizations():
    """Create sample visualizations with dummy data for testing"""
    
    print("\nCreating SAMPLE visualizations with dummy data...")
    
    # Sample waterfall data
    sample_shock = pd.DataFrame({
        'prov_num': [123456],
        'year': [2021],
        'income': [50_000_000],
        'rev_loss': [8_000_000],
        'net_savings': [3_500_000],
        'income_shocked_opt': [45_500_000]
    })
    
    create_waterfall_chart(sample_shock, save_path='sample_waterfall.png')
    
    # Sample frontier data
    np.random.seed(42)
    n = 500
    sample_frontier = pd.DataFrame({
        'opexp': np.random.lognormal(15, 0.5, n),
        'cases': np.random.lognormal(5, 0.8, n),
        'survival': np.random.beta(20, 2, n),
        'success': np.random.beta(18, 2, n),
        'medicaid_share': np.random.beta(2, 5, n),
        'efficiency': np.random.beta(5, 2, n),
        'on_frontier': (np.random.random(n) > 0.99).astype(int)
    })
    
    create_frontier_scatter(sample_frontier, save_path='sample_frontier_scatter.png')
    
    # Sample hero/struggler data
    sample_comparison = pd.DataFrame({
        'group': ['hero']*200 + ['struggler']*200 + ['middle']*200,
        'admin_share': np.concatenate([
            np.random.normal(0.132, 0.02, 200),
            np.random.normal(0.128, 0.02, 200),
            np.random.normal(0.123, 0.02, 200)
        ]),
        'nurse_intensity': np.concatenate([
            np.random.normal(338, 30, 200),
            np.random.normal(348, 30, 200),
            np.random.normal(297, 30, 200)
        ]),
        'occupancy': np.concatenate([
            np.random.normal(0.359, 0.05, 200),
            np.random.normal(0.641, 0.05, 200),
            np.random.normal(0.462, 0.05, 200)
        ]),
        'log_beds': np.concatenate([
            np.random.normal(4.15, 0.3, 200),
            np.random.normal(5.78, 0.3, 200),
            np.random.normal(4.97, 0.3, 200)
        ]),
        'margin': np.concatenate([
            np.random.normal(0.028, 0.01, 200),
            np.random.normal(0.039, 0.01, 200),
            np.random.normal(0.047, 0.01, 200)
        ])
    })
    
    create_hero_struggler_comparison(sample_comparison, 
                                     save_path='sample_hero_struggler.png')
    
    print("\nSample visualizations created successfully!")
    print("Check the generated PNG files to see the format.")

# Uncomment to test with sample data:
# create_sample_visualizations()