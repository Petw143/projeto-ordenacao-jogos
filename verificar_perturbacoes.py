#!/usr/bin/env python3
"""
Verificação visual das perturbações de 10% no vetor quase-ordenado
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from geradores import GeradorDados

def verificar_perturbacoes_detalhadamente():
    """Verificação detalhada das perturbações de 10%"""
    
    print("🔍 VERIFICAÇÃO DETALHADA DAS PERTURBAÇÕES DE 10%")
    print("=" * 60)
    
    # Usar tamanho pequeno para visualização clara
    tamanho = 20
    gerador = GeradorDados(seed=42)
    
    print(f"📊 Testando com {tamanho} elementos para visualização clara")
    print("=" * 60)
    
    # Gerar versão completamente ordenada para comparação
    dados_ordenados = list(range(1, tamanho + 1))
    print(f"✅ Dados completamente ordenados:")
    print(f"   {dados_ordenados}")
    
    # Gerar dados quase-ordenados
    dados_quase = gerador.gerar(tamanho, 'quase_ordenado')
    print(f"\n🔀 Dados quase-ordenados (com perturbações):")
    print(f"   {dados_quase}")
    
    # Identificar posições que foram perturbadas
    perturbacoes = []
    for i in range(tamanho):
        if dados_quase[i] != dados_ordenados[i]:
            perturbacoes.append(i)
    
    num_perturbacoes_esperado = int(tamanho * 0.1)
    num_perturbacoes_real = len(perturbacoes)
    
    print(f"\n📈 ANÁLISE DAS PERTURBAÇÕES:")
    print(f"   Perturbações esperadas (10%): {num_perturbacoes_esperado}")
    print(f"   Perturbações reais: {num_perturbacoes_real}")
    print(f"   Posições perturbadas: {perturbacoes}")
    
    # Mostrar as diferenças posição por posição
    print(f"\n🔎 COMPARAÇÃO POSIÇÃO POR POSIÇÃO:")
    print("   Pos | Ordenado | Quase-Ord | Status")
    print("   ----|----------|-----------|----------")
    
    for i in range(tamanho):
        status = "PERTURBADO" if i in perturbacoes else "OK"
        print(f"   {i:2d}  |    {dados_ordenados[i]:2d}    |    {dados_quase[i]:2d}     | {status}")
    
    # Calcular percentual real de perturbação
    percentual_real = (num_perturbacoes_real / tamanho) * 100
    print(f"\n📊 PERCENTUAL DE PERTURBAÇÃO:")
    print(f"   Esperado: 10.0%")
    print(f"   Real: {percentual_real:.1f}%")
    
    if 8 <= percentual_real <= 12:
        print("   ✅ PERTURBAÇÃO DENTRO DO ESPERADO!")
    else:
        print("   ⚠️  Perturbação fora do esperado")

def teste_tamanho_maior():
    """Teste com tamanho maior para estatísticas mais precisas"""
    
    print(f"\n" + "=" * 60)
    print("🔍 TESTE COM TAMANHO MAIOR (1000 elementos)")
    print("=" * 60)
    
    tamanho = 1000
    gerador = GeradorDados(seed=42)
    
    # Gerar dados quase-ordenados
    dados_quase = gerador.gerar(tamanho, 'quase_ordenado')
    dados_ordenados = sorted(dados_quase.copy())
    
    # Contar elementos fora de posição
    elementos_fora_posicao = 0
    for i in range(tamanho):
        if dados_quase[i] != dados_ordenados[i]:
            elementos_fora_posicao += 1
    
    percentual_perturbacao = (elementos_fora_posicao / tamanho) * 100
    
    print(f"📊 ESTATÍSTICAS FINAIS:")
    print(f"   Total de elementos: {tamanho}")
    print(f"   Elementos fora de posição: {elementos_fora_posicao}")
    print(f"   Percentual de perturbação: {percentual_perturbacao:.2f}%")
    print(f"   Meta: 10.0%")
    
    if 8 <= percentual_perturbacao <= 12:
        print("   ✅ ALGORITMO FUNCIONANDO CORRETAMENTE!")
    else:
        print("   ⚠️  Algoritmo pode precisar de ajuste")

def mostrar_codigo_perturbacao():
    """Mostrar exatamente onde no código acontecem as perturbações"""
    
    print(f"\n" + "=" * 60)
    print("💻 ONDE VER AS PERTURBAÇÕES NO CÓDIGO")
    print("=" * 60)
    
    print("📁 Arquivo: src/geradores.py")
    print("🔍 Função: _gerar_quase_ordenado()")
    print("📍 Linhas específicas onde acontecem as perturbações:")
    print()
    print("```python")
    print("# ETAPA 4: Aplicar perturbações aleatórias (10% dos dados)")
    print("num_perturbacoes = int(tamanho * 0.1)")
    print("posicoes_perturbacao = random.sample(range(tamanho), num_perturbacoes)")
    print("")
    print("# Aplicar perturbações (trocar elementos de posição)")
    print("for i in posicoes_perturbacao:")
    print("    # Escolher nova posição aleatória")
    print("    j = random.randint(0, tamanho - 1)")
    print("    # Trocar elementos")
    print("    dados_ordenados[i], dados_ordenados[j] = dados_ordenados[j], dados_ordenados[i]")
    print("```")
    print()
    print("🎯 COMO VERIFICAR MANUALMENTE:")
    print("1. Abra o arquivo: src/geradores.py")
    print("2. Vá para a linha ~87-95 (método _gerar_quase_ordenado)")
    print("3. Adicione print() para ver as perturbações:")
    print("   print(f'Perturbando posição {i} com posição {j}')")
    print("4. Execute novamente o teste")

if __name__ == "__main__":
    # Executar verificações
    verificar_perturbacoes_detalhadamente()
    teste_tamanho_maior()
    mostrar_codigo_perturbacao()
    
    print(f"\n🏁 VERIFICAÇÃO CONCLUÍDA!")
    print("🔍 Agora você pode ver exatamente onde e como as perturbações acontecem!")
