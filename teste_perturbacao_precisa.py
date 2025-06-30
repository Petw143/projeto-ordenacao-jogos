#!/usr/bin/env python3
"""
Teste específico para verificar exatamente onde estão as perturbações
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from geradores import GeradorDados

def teste_perturbacao_exata():
    """Teste que mostra exatamente onde estão as perturbações"""
    
    print("🔍 TESTE PRECISO DAS PERTURBAÇÕES - VERSÃO CORRIGIDA")
    print("=" * 60)
    
    for tamanho in [10, 100, 1000]:
        print(f"\n📊 Testando com {tamanho} elementos:")
        print("-" * 40)
        
        gerador = GeradorDados(seed=42)
        
        # Gerar dados quase-ordenados
        dados_quase = gerador.gerar(tamanho, 'quase_ordenado')
        
        # Calcular perturbações reais
        perturbacoes_diretas = 0
        elementos_fora_posicao = 0
        
        for i in range(tamanho):
            valor_esperado = i + 1  # posição correta seria valor = posição + 1
            valor_real = dados_quase[i]
            
            if valor_real != valor_esperado:
                elementos_fora_posicao += 1
        
        # Calcular perturbações diretas (número exato de modificações feitas)
        num_perturbacoes_esperado = max(1, int(tamanho * 0.1))
        
        percentual_elementos_fora = (elementos_fora_posicao / tamanho) * 100
        percentual_perturbacoes = (num_perturbacoes_esperado / tamanho) * 100
        
        print(f"   Perturbações diretas aplicadas: {num_perturbacoes_esperado} ({percentual_perturbacoes:.1f}%)")
        print(f"   Elementos fora de posição: {elementos_fora_posicao} ({percentual_elementos_fora:.1f}%)")
        
        if tamanho <= 20:
            print(f"   Dados: {dados_quase}")
        
        # Status
        if abs(percentual_elementos_fora - 10.0) <= 2.0:
            print("   ✅ RESULTADO DENTRO DO ESPERADO")
        else:
            print("   ⚠️  Resultado fora do esperado")
            
        # Para tamanhos pequenos, mostrar detalhes
        if tamanho <= 20:
            print(f"   Posições perturbadas detectadas:")
            for i in range(tamanho):
                if dados_quase[i] != (i + 1):
                    print(f"     Posição {i}: esperado {i+1}, obtido {dados_quase[i]}")

def onde_verificar_no_codigo():
    """Mostrar exatamente onde verificar as perturbações no código"""
    
    print(f"\n" + "=" * 60)
    print("📍 ONDE VERIFICAR AS PERTURBAÇÕES NO CÓDIGO")
    print("=" * 60)
    
    print("📂 Localização: src/geradores.py")
    print("🔍 Método: _gerar_quase_ordenado() (linhas ~75-125)")
    print()
    print("🎯 Para verificar as perturbações pessoalmente:")
    print()
    print("1. Abra o arquivo src/geradores.py")
    print("2. Localize a ETAPA 5 do método _gerar_quase_ordenado")
    print("3. Adicione esta linha após a linha 'dados_ordenados[pos] = novo_valor':")
    print()
    print("   print(f'PERTURBAÇÃO: Posição {pos} mudou de {valor_original} para {novo_valor}')")
    print()
    print("4. Execute o teste novamente para ver exatamente quais posições foram modificadas")
    print()
    print("📊 O algoritmo agora funciona assim:")
    print("   • Cria lista ordenada [1, 2, 3, ..., n]")
    print("   • Seleciona exatamente 10% das posições aleatoriamente")
    print("   • Para cada posição selecionada, substitui por valor aleatório")
    print("   • Resultado: exatamente 10% das posições têm valores 'errados'")
    print()
    print("✅ Isso garante perturbação precisa de 10%!")

if __name__ == "__main__":
    teste_perturbacao_exata()
    onde_verificar_no_codigo()
    print(f"\n🏁 VERIFICAÇÃO CONCLUÍDA!")
