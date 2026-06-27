#!/usr/bin/env python3
"""
Script per analizzare e visualizzare le competenze dal file test.xlsx
Genera: BarChart, Heatmap, Radar Chart
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties

# Impostazioni generali
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Carico i dati
df = pd.read_excel('test.xlsx')

# Pulizia nomi colonne (rimuovo spazi finali)
df.columns = df.columns.str.strip()

# Lista delle competenze (escludo Individuo, Tipologia, media complessiva)
competenze = [col for col in df.columns if col not in ['Individuo', 'Tipologia', 'media complessiva']]

print("=" * 80)
print("ANALISI COMPETENZE - DASHBOARD")
print("=" * 80)
print(f"\nDataset: {len(df)} individui")
print(f"Competenze analizzate: {len(competenze)}")
print(f"Tipologie: {df['Tipologia'].nunique()}")
print(f"\nTipologie:")
for tipologia, count in df['Tipologia'].value_counts().items():
    print(f"  - {tipologia}: {count} individui")

# ============================================================================
# 1. BAR CHART - Media per competenza
# ============================================================================
print("\n" + "=" * 80)
print("GENERAZIONE GRAFICI")
print("=" * 80)

print("\n1. Bar Chart - Media per competenza...")

# Calcolo medie per competenza
medie_competenze = df[competenze].mean().sort_values(ascending=False)

# Creo il grafico
fig, ax = plt.subplots(figsize=(14, 8))

# Ordino le competenze per media decrescente
medie_competenze_sorted = medie_competenze.sort_values(ascending=True)

# Creo il bar chart
bars = ax.barh(medie_competenze_sorted.index, medie_competenze_sorted.values, 
               color=sns.color_palette("viridis", len(competenze)))

# Aggiungo le etichette con i valori
for i, (competenza, media) in enumerate(medie_competenze_sorted.items()):
    ax.text(media + 0.05, i, f'{media:.2f}', va='center', fontsize=10)

# Personalizzazione
ax.set_xlabel('Media (scala 1-4)', fontsize=12, fontweight='bold')
ax.set_ylabel('Competenza', fontsize=12, fontweight='bold')
ax.set_title('Media delle Competenze (Tutti gli Individui)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(0, 4.5)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Aggiungo la media complessiva come linea verticale
media_totale = df['media complessiva'].mean()
ax.axvline(x=media_totale, color='red', linestyle='--', 
           label=f'Media complessiva: {media_totale:.2f}')
ax.legend()

plt.tight_layout()
plt.savefig('barchart_media_competenze.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Bar Chart salvato come 'barchart_media_competenze.png'")

# ============================================================================
# 2. BAR CHART - Media per tipologia
# ============================================================================
print("2. Bar Chart - Media per tipologia...")

# Calcolo medie per tipologia
medie_tipologia = df.groupby('Tipologia')[competenze].mean()

# Creo un grafico per ogni competenza
fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(20, 16))
axes = axes.flatten()

for idx, competenza in enumerate(competenze):
    if idx < len(axes):
        # Ordino per media
        medie_comp_sorted = medie_tipologia[competenza].sort_values(ascending=False)
        
        # Creo il bar chart
        bars = axes[idx].bar(medie_comp_sorted.index, medie_comp_sorted.values,
                            color=sns.color_palette("Set2", len(medie_comp_sorted)))
        
        # Aggiungo etichette
        for i, (tipologia, media) in enumerate(medie_comp_sorted.items()):
            axes[idx].text(i, media + 0.05, f'{media:.2f}', 
                          ha='center', fontsize=9)
        
        axes[idx].set_title(competenza, fontsize=10, fontweight='bold')
        axes[idx].set_ylim(0, 4.5)
        axes[idx].set_xticklabels(axes[idx].get_xticklabels(), rotation=45, ha='right', fontsize=8)
        axes[idx].grid(axis='y', alpha=0.3, linestyle='--')

# Nascondo gli assi inutilizzati
for idx in range(len(competenze), len(axes)):
    axes[idx].axis('off')

plt.suptitle('Media delle Competenze per Tipologia', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('barchart_media_per_tipologia.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Bar Chart per tipologia salvato come 'barchart_media_per_tipologia.png'")

# ============================================================================
# 3. HEATMAP - Matrice di correlazione
# ============================================================================
print("3. Heatmap - Matrice di correlazione...")

# Calcolo la matrice di correlazione
corr_matrix = df[competenze].corr()

# Creo l'heatmap
fig, ax = plt.subplots(figsize=(14, 12))

# Creo una maschera per il triangolo superiore
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Heatmap con annotazioni
sns.heatmap(corr_matrix, 
            mask=mask,
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm', 
            center=0, 
            square=True, 
            linewidths=0.5, 
            cbar_kws={'shrink': 0.8, 'label': 'Coefficiente di correlazione'},
            ax=ax,
            annot_kws={'size': 9})

# Personalizzazione
ax.set_title('Matrice di Correlazione tra Competenze', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout()
plt.savefig('heatmap_correlazione_competenze.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Heatmap salvata come 'heatmap_correlazione_competenze.png'")

# ============================================================================
# 4. HEATMAP - Distribuzione dei punteggi per competenza e tipologia
# ============================================================================
print("4. Heatmap - Distribuzione punteggi per competenza e tipologia...")

# Pivot table: tipologia vs competenza con media
pivot_table = df.pivot_table(index='Tipologia', columns='Individuo', 
                             values=competenze, aggfunc='mean')

# Oppure: media per tipologia e competenza
pivot_comp_tipologia = df.groupby('Tipologia')[competenze].mean().T

fig, ax = plt.subplots(figsize=(14, 8))

# Heatmap
sns.heatmap(pivot_comp_tipologia, 
            annot=True, 
            fmt='.2f', 
            cmap='YlGnBu', 
            ax=ax,
            cbar_kws={'label': 'Punteggio medio'},
            annot_kws={'size': 10})

# Personalizzazione
ax.set_title('Punteggi Medi per Competenza e Tipologia', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Tipologia', fontsize=12, fontweight='bold')
ax.set_ylabel('Competenza', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('heatmap_punteggi_tipologia.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Heatmap punteggi salvata come 'heatmap_punteggi_tipologia.png'")

# ============================================================================
# 5. RADAR CHART - Confronto tra tipologie
# ============================================================================
print("5. Radar Chart - Confronto tra tipologie...")

# Dati per il radar chart
categories = competenze
N = len(categories)

# Calcolo medie per tipologia
medie_per_tipologia = df.groupby('Tipologia')[competenze].mean()

# Angoli per il radar chart
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Creo il radar chart
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'polar': True})

# Colori per ogni tipologia
colors = plt.cm.tab10(np.linspace(0, 1, len(medie_per_tipologia)))

# Plot per ogni tipologia
for idx, (tipologia, row) in enumerate(medie_per_tipologia.iterrows()):
    values = row.values.tolist()
    values += values[:1]
    
    ax.plot(angles, values, color=colors[idx], linewidth=2, 
            linestyle='solid', label=tipologia)
    ax.fill(angles, values, color=colors[idx], alpha=0.25)

# Personalizzazione
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Etichette delle competenze
plt.xticks(angles[:-1], categories, size=10)

# Etichette dei valori
ax.set_rlabel_position(0)
plt.yticks([2, 2.5, 3, 3.5, 4, 4.5], ["2.0", "2.5", "3.0", "3.5", "4.0", "4.5"], 
          color="grey", size=10)
plt.ylim(0, 4.5)

# Titolo e legenda
plt.title('Radar Chart: Confronto Competenze per Tipologia', 
          size=16, fontweight='bold', y=1.1)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig('radar_chart_tipologie.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Radar Chart salvato come 'radar_chart_tipologie.png'")

# ============================================================================
# 6. RADAR CHART - Singolo individuo (esempio)
# ============================================================================
print("6. Radar Chart - Esempio singolo individuo...")

# Seleziono un individuo a caso
individuo_esempio = df.iloc[0]

# Dati per il radar chart
values = individuo_esempio[competenze].values.tolist()
values += values[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'polar': True})

# Plot
ax.plot(angles, values, color='blue', linewidth=2, linestyle='solid', 
        label=f"{individuo_esempio['Individuo']} ({individuo_esempio['Tipologia']})")
ax.fill(angles, values, color='blue', alpha=0.25)

# Aggiungo la media della sua tipologia per confronto
media_tipologia = medie_per_tipologia.loc[individuo_esempio['Tipologia']].values.tolist()
media_tipologia += media_tipologia[:1]
ax.plot(angles, media_tipologia, color='red', linewidth=2, 
        linestyle='--', label=f"Media {individuo_esempio['Tipologia']}")

# Personalizzazione
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories, size=10)
ax.set_rlabel_position(0)
plt.yticks([2, 2.5, 3, 3.5, 4, 4.5], ["2.0", "2.5", "3.0", "3.5", "4.0", "4.5"], 
          color="grey", size=10)
plt.ylim(0, 4.5)

plt.title(f'Radar Chart: {individuo_esempio["Individuo"]}', 
          size=14, fontweight='bold', y=1.1)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig('radar_chart_individuo_esempio.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"   ✓ Radar Chart individuo salvato come 'radar_chart_individuo_esempio.png'")

# ============================================================================
# 7. ANALISI STATISTICA DETTAGLIATA
# ============================================================================
print("\n" + "=" * 80)
print("ANALISI STATISTICA DETTAGLIATA")
print("=" * 80)

# Statistiche per competenza
print("\nStatistiche per competenza:")
stats_competenze = df[competenze].describe().T
stats_competenze['range'] = stats_competenze['max'] - stats_competenze['min']
print(stats_competenze.to_string())

# Statistiche per tipologia
print("\nStatistiche per tipologia:")
for tipologia in df['Tipologia'].unique():
    df_tip = df[df['Tipologia'] == tipologia]
    print(f"\n--- {tipologia} ({len(df_tip)} individui) ---")
    print(f"Media complessiva: {df_tip['media complessiva'].mean():.2f} ± {df_tip['media complessiva'].std():.2f}")
    
    # Top 3 competenze
    medie_comp = df_tip[competenze].mean().sort_values(ascending=False)
    print("Top 3 competenze:")
    for comp, media in medie_comp.head(3).items():
        print(f"  {comp}: {media:.2f}")
    
    # Bottom 3 competenze
    print("Bottom 3 competenze:")
    for comp, media in medie_comp.tail(3).items():
        print(f"  {comp}: {media:.2f}")

# ============================================================================
# 8. SALVATAGGIO DATI ELABORATI
# ============================================================================
print("\n" + "=" * 80)
print("SALVATAGGIO DATI ELABORATI")
print("=" * 80)

# Salvo i dati elaborati in un nuovo file Excel
with pd.ExcelWriter('analisi_competenze.xlsx') as writer:
    # Dati originali
    df.to_excel(writer, sheet_name='Dati Originali', index=False)
    
    # Statistiche per competenza
    stats_competenze.to_excel(writer, sheet_name='Statistiche Competenze')
    
    # Medie per tipologia
    medie_per_tipologia.to_excel(writer, sheet_name='Medie per Tipologia')
    
    # Matrice di correlazione
    corr_matrix.to_excel(writer, sheet_name='Correlazione')

print("✓ Dati elaborati salvati in 'analisi_competenze.xlsx'")

print("\n" + "=" * 80)
print("ANALISI COMPLETATA!")
print("=" * 80)
print("\nFile generati:")
print("  - barchart_media_competenze.png")
print("  - barchart_media_per_tipologia.png")
print("  - heatmap_correlazione_competenze.png")
print("  - heatmap_punteggi_tipologia.png")
print("  - radar_chart_tipologie.png")
print("  - radar_chart_individuo_esempio.png")
print("  - analisi_competenze.xlsx")
