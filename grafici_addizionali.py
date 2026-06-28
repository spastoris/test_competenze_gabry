#!/usr/bin/env python3
"""
Script per generare grafici addizionali:
1. Bar chart media per competenza - Dirigenti (Milano + Avezzano)
2. Bar chart media per competenza - Professional (Milano + Avezzano)
3. Classifica media competenze per individuo per ogni gruppo
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Impostazioni generali
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Carico i dati
df = pd.read_excel('test.xlsx')

# Pulizia nomi colonne
df.columns = df.columns.str.strip()

# Lista delle competenze
competenze = [col for col in df.columns if col not in ['Individuo', 'Tipologia', 'media complessiva']]

print("=" * 80)
print("GENERAZIONE GRAFICI ADDIZIONALI")
print("=" * 80)

# ============================================================================
# 1. BAR CHART - Media per competenza DIRIGENTI (Milano + Avezzano)
# ============================================================================
print("\n1. Bar Chart - Media per competenza DIRIGENTI...")

# Filtro solo dirigenti
df_dirigenti = df[df['Tipologia'].str.contains('Dirigente')]

# Calcolo medie per competenza
medie_dirigenti = df_dirigenti[competenze].mean().sort_values(ascending=True)

# Creo il grafico
fig, ax = plt.subplots(figsize=(14, 8))

# Bar chart
bars = ax.barh(medie_dirigenti.index, medie_dirigenti.values, 
               color=sns.color_palette("Blues_d", len(competenze)))

# Aggiungo le etichette con i valori
for i, (competenza, media) in enumerate(medie_dirigenti.items()):
    ax.text(media + 0.05, i, f'{media:.2f}', va='center', fontsize=10)

# Personalizzazione
ax.set_xlabel('Media (scala 1-4)', fontsize=12, fontweight='bold')
ax.set_ylabel('Competenza', fontsize=12, fontweight='bold')
ax.set_title('Media delle Competenze - DIRIGENTI (Milano + Avezzano)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(0, 4.5)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Aggiungo la media complessiva come linea verticale
media_totale_dirigenti = df_dirigenti['media complessiva'].mean()
ax.axvline(x=media_totale_dirigenti, color='red', linestyle='--', 
           label=f'Media complessiva: {media_totale_dirigenti:.2f}')
ax.legend()

plt.tight_layout()
plt.savefig('barchart_media_competenze_dirigenti.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Bar Chart Dirigenti salvato come 'barchart_media_competenze_dirigenti.png'")

# ============================================================================
# 2. BAR CHART - Media per competenza PROFESSIONAL (Milano + Avezzano)
# ============================================================================
print("2. Bar Chart - Media per competenza PROFESSIONAL...")

# Filtro solo professional
df_professional = df[df['Tipologia'].str.contains('Professional')]

# Calcolo medie per competenza
medie_professional = df_professional[competenze].mean().sort_values(ascending=True)

# Creo il grafico
fig, ax = plt.subplots(figsize=(14, 8))

# Bar chart
bars = ax.barh(medie_professional.index, medie_professional.values, 
               color=sns.color_palette("Greens_d", len(competenze)))

# Aggiungo le etichette con i valori
for i, (competenza, media) in enumerate(medie_professional.items()):
    ax.text(media + 0.05, i, f'{media:.2f}', va='center', fontsize=10)

# Personalizzazione
ax.set_xlabel('Media (scala 1-4)', fontsize=12, fontweight='bold')
ax.set_ylabel('Competenza', fontsize=12, fontweight='bold')
ax.set_title('Media delle Competenze - PROFESSIONAL (Milano + Avezzano)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(0, 4.5)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Aggiungo la media complessiva come linea verticale
media_totale_professional = df_professional['media complessiva'].mean()
ax.axvline(x=media_totale_professional, color='red', linestyle='--', 
           label=f'Media complessiva: {media_totale_professional:.2f}')
ax.legend()

plt.tight_layout()
plt.savefig('barchart_media_competenze_professional.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Bar Chart Professional salvato come 'barchart_media_competenze_professional.png'")

# ============================================================================
# 3. CLASSIFICA - Media competenze per individuo per ogni gruppo
# ============================================================================
print("3. Classifica media competenze per individuo per ogni gruppo...")

# Creo un DataFrame con le medie per ogni individuo
df_classifica = df[['Individuo', 'Tipologia', 'media complessiva']].copy()
df_classifica = df_classifica.rename(columns={'media complessiva': 'Media'})

# Ordino per media decrescente all'interno di ogni gruppo
df_classifica['Rank'] = df_classifica.groupby('Tipologia')['Media'].rank(ascending=False, method='min')

# Aggiungo anche la media del gruppo
df_classifica['Media Gruppo'] = df_classifica['Tipologia'].map(
    df.groupby('Tipologia')['media complessiva'].mean()
)

# Creo il grafico
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 16))
axes = axes.flatten()

# Colori per i gruppi
colors = {
    'Dirigente Milano': 'blue',
    'Dirigente Avezzano': 'green',
    'Professional Milano': 'orange',
    'Professional Avezzano': 'purple'
}

# Per ogni gruppo
for idx, tipologia in enumerate(df['Tipologia'].unique()):
    df_gruppo = df_classifica[df_classifica['Tipologia'] == tipologia].sort_values('Media', ascending=False)
    
    # Creo il bar chart
    bars = axes[idx].barh(df_gruppo['Individuo'], df_gruppo['Media'], 
                         color=colors[tipologia], alpha=0.7)
    
    # Aggiungo la linea della media del gruppo
    media_gruppo = df_gruppo['Media Gruppo'].iloc[0]
    axes[idx].axvline(x=media_gruppo, color='red', linestyle='--', 
                     label=f'Media gruppo: {media_gruppo:.2f}')
    
    # Aggiungo le etichette con i valori
    for i, (_, row) in enumerate(df_gruppo.iterrows()):
        axes[idx].text(row['Media'] + 0.02, i, f'{row["Media"]:.2f}', 
                      va='center', fontsize=8)
    
    # Personalizzazione
    axes[idx].set_xlabel('Media', fontsize=10, fontweight='bold')
    axes[idx].set_ylabel('Individuo', fontsize=10, fontweight='bold')
    axes[idx].set_title(f'Classifica {tipologia} ({len(df_gruppo)} individui)', 
                       fontsize=12, fontweight='bold')
    axes[idx].set_xlim(0, 4.5)
    axes[idx].grid(axis='x', alpha=0.3, linestyle='--')
    axes[idx].legend(fontsize=8)
    
    # Ruoto le etichette sull'asse y per leggibilita
    axes[idx].set_yticklabels(df_gruppo['Individuo'], fontsize=8)

# Nascondo gli assi inutilizzati
for idx in range(len(df['Tipologia'].unique()), len(axes)):
    axes[idx].axis('off')

plt.suptitle('Classifica Media Competenze per Individuo - Per Gruppo', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('classifica_media_competenze_per_gruppo.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Classifica salvata come 'classifica_media_competenze_per_gruppo.png'")

# ============================================================================
# 4. CLASSIFICA UNICA CON TUTTI I GRUPPI
# ============================================================================
print("4. Classifica unica con tutti i gruppi...")

# Ordino tutti gli individui per media decrescente
df_classifica_totale = df_classifica.sort_values('Media', ascending=False)

# Creo il grafico
fig, ax = plt.subplots(figsize=(16, 12))

# Colori basati sul gruppo
for tipologia in df['Tipologia'].unique():
    df_tip = df_classifica_totale[df_classifica_totale['Tipologia'] == tipologia]
    ax.barh(df_tip['Individuo'], df_tip['Media'], 
            color=colors[tipologia], alpha=0.7, label=tipologia)

# Aggiungo le etichette con i valori
for i, (_, row) in enumerate(df_classifica_totale.iterrows()):
    ax.text(row['Media'] + 0.02, i, f'{row["Media"]:.2f}', 
            va='center', fontsize=8)

# Personalizzazione
ax.set_xlabel('Media', fontsize=12, fontweight='bold')
ax.set_ylabel('Individuo', fontsize=12, fontweight='bold')
ax.set_title('Classifica Globale - Media Competenze per Individuo', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 4.5)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.legend(title='Gruppo', fontsize=10)

plt.tight_layout()
plt.savefig('classifica_globale_media_competenze.png', dpi=300, bbox_inches='tight')
plt.close()

print("   ✓ Classifica globale salvata come 'classifica_globale_media_competenze.png'")

# ============================================================================
# 5. TABELLA CLASSIFICA (salvataggio su file)
# ============================================================================
print("5. Salvataggio tabella classifica...")

# Salvo la classifica su Excel
with pd.ExcelWriter('classifica_competenze.xlsx') as writer:
    # Classifica per gruppo
    for tipologia in df['Tipologia'].unique():
        df_tip = df_classifica[df_classifica['Tipologia'] == tipologia].sort_values('Media', ascending=False)
        df_tip.to_excel(writer, sheet_name=tipologia.replace(' ', '_'), index=False)
    
    # Classifica globale
    df_classifica_totale.to_excel(writer, sheet_name='Classifica_Globale', index=False)

print("   ✓ Tabella classifica salvata come 'classifica_competenze.xlsx'")

print("\n" + "=" * 80)
print("GENERAZIONE COMPLETATA!")
print("=" * 80)

# Elenco tutti i file generati
import os
files = [f for f in os.listdir() if f.startswith(('barchart_media_competenze_', 'classifica_')) and f.endswith(('.png', '.xlsx'))]
print(f"\nFile generati ({len(files)}):")
for f in sorted(files):
    size = os.path.getsize(f) / 1024  # KB
    print(f"  - {f} ({size:.1f} KB)")
