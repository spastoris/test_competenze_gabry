#!/usr/bin/env python3
"""
Script per generare radar chart individuali per ogni persona
con confronto alla media del proprio gruppo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# Impostazioni generali
plt.style.use('seaborn-v0_8')

# Carico i dati
df = pd.read_excel('test.xlsx')

# Pulizia nomi colonne
df.columns = df.columns.str.strip()

# Lista delle competenze (escludo Individuo, Tipologia, media complessiva)
competenze = [col for col in df.columns if col not in ['Individuo', 'Tipologia', 'media complessiva']]

# Calcolo medie per tipologia
medie_per_tipologia = df.groupby('Tipologia')[competenze].mean()

# Angoli per il radar chart
N = len(competenze)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

print("=" * 80)
print("GENERAZIONE RADAR CHART INDIVIDUALI")
print("=" * 80)

# ============================================================================
# 1. RADAR CHART PER OGNI INDIVIDUO (singoli file)
# ============================================================================
print("\n1. Generazione radar chart individuali...")

for idx, row in df.iterrows():
    individuo = row['Individuo']
    tipologia = row['Tipologia']
    
    # Dati individuo
    values_individuo = row[competenze].values.tolist()
    values_individuo += values_individuo[:1]
    
    # Dati media gruppo
    media_gruppo = medie_per_tipologia.loc[tipologia].values.tolist()
    media_gruppo += media_gruppo[:1]
    
    # Creo il radar chart
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'polar': True})
    
    # Plot individuo
    ax.plot(angles, values_individuo, color='blue', linewidth=2, 
            linestyle='solid', label=f'{individuo}')
    ax.fill(angles, values_individuo, color='blue', alpha=0.25)
    
    # Plot media gruppo
    ax.plot(angles, media_gruppo, color='red', linewidth=2, 
            linestyle='--', label=f'Media {tipologia}')
    ax.fill(angles, media_gruppo, color='red', alpha=0.15)
    
    # Personalizzazione
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Etichette delle competenze (accorcio i nomi se troppo lunghi)
    competenze_short = [comp.replace(' ', '\n') for comp in competenze]
    plt.xticks(angles[:-1], competenze_short, size=10)
    
    # Etichette dei valori
    ax.set_rlabel_position(0)
    plt.yticks([2, 2.5, 3, 3.5, 4, 4.5], ["2.0", "2.5", "3.0", "3.5", "4.0", "4.5"], 
              color="grey", size=10)
    plt.ylim(0, 4.5)
    
    # Titolo
    plt.title(f'Radar Chart: {individuo}\n({tipologia})', 
              size=14, fontweight='bold', y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    plt.tight_layout()
    
    # Salvo il file
    filename = f'radar_chart_{tipologia.replace(" ", "_")}_{individuo.replace(" ", "_")}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ {filename}")

print("\n   Tutti i radar chart individuali generati!")

# ============================================================================
# 2. RADAR CHART PER GRUPPO (tutti gli individui in un'unica immagine)
# ============================================================================
print("\n2. Generazione radar chart per gruppo...")

# Colori per i gruppi
colors = {
    'Dirigente Milano': 'blue',
    'Dirigente Avezzano': 'green',
    'Professional Milano': 'orange',
    'Professional Avezzano': 'purple'
}

# Per ogni gruppo
for tipologia in df['Tipologia'].unique():
    df_gruppo = df[df['Tipologia'] == tipologia]
    
    # Calcolo quante righe e colonne servono
    n_individui = len(df_gruppo)
    
    # Dimensione della griglia
    if n_individui <= 4:
        n_cols = 2
        n_rows = int(np.ceil(n_individui / n_cols))
    elif n_individui <= 9:
        n_cols = 3
        n_rows = int(np.ceil(n_individui / n_cols))
    else:
        n_cols = 4
        n_rows = int(np.ceil(n_individui / n_cols))
    
    # Creo la figura
    fig = plt.figure(figsize=(n_cols * 8, n_rows * 8))
    
    # Aggiungo il titolo generale
    fig.suptitle(f'Radar Chart - {tipologia} ({n_individui} individui)', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Per ogni individuo nel gruppo
    for idx, (_, row) in enumerate(df_gruppo.iterrows()):
        ax = fig.add_subplot(n_rows, n_cols, idx + 1, polar=True)
        
        # Dati individuo
        values_individuo = row[competenze].values.tolist()
        values_individuo += values_individuo[:1]
        
        # Dati media gruppo
        media_gruppo = medie_per_tipologia.loc[tipologia].values.tolist()
        media_gruppo += media_gruppo[:1]
        
        # Plot individuo
        ax.plot(angles, values_individuo, color=colors[tipologia], linewidth=2, 
                linestyle='solid', label=row['Individuo'][:20])
        ax.fill(angles, values_individuo, color=colors[tipologia], alpha=0.25)
        
        # Plot media gruppo
        ax.plot(angles, media_gruppo, color='red', linewidth=1.5, 
                linestyle='--', label='Media gruppo')
        
        # Personalizzazione
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Etichette solo per il primo subplot per evitare sovrapposizioni
        if idx == 0:
            competenze_short = [comp.replace(' ', '\n') for comp in competenze]
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(competenze_short, size=8)
            ax.set_rlabel_position(0)
            plt.yticks([2, 2.5, 3, 3.5, 4, 4.5], ["2.0", "2.5", "3.0", "3.5", "4.0", "4.5"], 
                      color="grey", size=8)
            plt.ylim(0, 4.5)
        else:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        
        # Titolo del subplot
        ax.set_title(f"{row['Individuo']}", size=10, fontweight='bold', y=1.1)
        
        # Legenda solo per il primo
        if idx == 0:
            ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=8)
    
    plt.tight_layout()
    
    # Salvo il file
    filename = f'radar_chart_gruppo_{tipologia.replace(" ", "_")}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✓ {filename} ({n_individui} individui)")

print("\n" + "=" * 80)
print("GENERAZIONE COMPLETATA!")
print("=" * 80)

# Elenco tutti i file generati
import os
files = [f for f in os.listdir() if f.startswith('radar_chart_') and f.endswith('.png')]
print(f"\nFile generati ({len(files)}):")
for f in sorted(files):
    size = os.path.getsize(f) / 1024  # KB
    print(f"  - {f} ({size:.1f} KB)")
