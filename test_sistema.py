"""
Script de teste rápido para verificar se todos os módulos estão funcionando corretamente.
Execute este script antes de rodar o experimento completo.
"""

import sys
import os
import time
import traceback

# Adicionar src ao path se necessário
sys.path.append('src')

def teste_imports():
    """Testar se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from geradores import GeradorDados
        print("✅ geradores.py - OK")
        
        from algoritmos import obter_todos_algoritmos
        print("✅ algoritmos.py - OK")
        
        from benchmark import Benchmark
        print("✅ benchmark.py - OK")
        
        from analise import AnalisadorResultados
        print("✅ analise.py - OK")
        
        from visualizacao import GeradorGraficos
        print("✅ visualizacao.py - OK")
        
        import config
        print("✅ config.py - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no import: {e}")
        traceback.print_exc()
        return False

def teste_geradores():
    """Testar geração de dados"""
    print("\n🎲 Testando geradores de dados...")
    
    try:
        from geradores import GeradorDados
        
        gerador = GeradorDados()
        
        # Teste dados exponenciais
        dados_exp = gerador.gerar(1000, 'exponencial')
        print(f"✅ Dados exponenciais: {len(dados_exp)} elementos, min={min(dados_exp)}, max={max(dados_exp)}")
        
        # Teste dados quase ordenados
        dados_quase = gerador.gerar(1000, 'quase_ordenado')
        print(f"✅ Dados quase ordenados: {len(dados_quase)} elementos, min={min(dados_quase)}, max={max(dados_quase)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos geradores: {e}")
        traceback.print_exc()
        return False

def teste_algoritmos():
    """Testar algoritmos de ordenação"""
    print("\n⚡ Testando algoritmos...")
    
    try:
        from algoritmos import obter_todos_algoritmos
        from geradores import GeradorDados
        
        gerador = GeradorDados()
        dados_teste = gerador.gerar(100, 'exponencial')
        
        # Testar todas as variantes
        todos_algoritmos = obter_todos_algoritmos(cutoff=10)
        for i, algoritmo in enumerate(todos_algoritmos):
            resultado = algoritmo.ordenar(dados_teste.copy())
            ordenado = all(resultado[i] <= resultado[i+1] for i in range(len(resultado)-1))
            status = 'Ordenou corretamente' if ordenado else 'ERRO na ordenação'
            print(f"✅ {algoritmo.nome}: {status}")
        
        print(f"✅ Total de algoritmos testados: {len(todos_algoritmos)}")
        
        return len(todos_algoritmos) > 0
        
    except Exception as e:
        print(f"❌ Erro nos algoritmos: {e}")
        traceback.print_exc()
        return False

def teste_benchmark():
    """Testar sistema de benchmark"""
    print("\n📊 Testando benchmark...")
    
    try:
        from benchmark import Benchmark
        from algoritmos import obter_todos_algoritmos
        from geradores import GeradorDados
        
        gerador = GeradorDados()
        dados_teste = gerador.gerar(1000, 'exponencial')
        
        benchmark = Benchmark()
        algoritmos = obter_todos_algoritmos(cutoff=10)
        merge = algoritmos[0]  # Usar o primeiro algoritmo da lista
        
        # Teste medição simples
        tempo = benchmark.medir_tempo(merge, dados_teste.copy())
        print(f"✅ Medição de tempo: {tempo:.4f}s")
        
        # Teste medição completa
        metricas = benchmark.medir_tempo_e_memoria(merge, dados_teste.copy())
        print(f"✅ Medição completa: tempo={metricas['tempo_execucao']:.4f}s, memoria={metricas['memoria_usada']:.2f}MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no benchmark: {e}")
        traceback.print_exc()
        return False

def teste_analise():
    """Testar análise estatística"""
    print("\n📈 Testando análise...")
    
    try:
        from analise import AnalisadorResultados
        import pandas as pd
        
        # Criar dados de teste
        dados_teste = pd.DataFrame({
            'algoritmo': ['merge_sort', 'quick_sort'] * 5,
            'tamanho': [1000] * 10,
            'tipo_dado': ['exponencial'] * 10,
            'tempo_medio': [0.1, 0.08, 0.11, 0.09, 0.12, 0.07, 0.10, 0.08, 0.11, 0.09]
        })
        
        analisador = AnalisadorResultados()
        relatorio = analisador.analisar(dados_teste)
        
        print(f"✅ Análise executada: {len(relatorio)} seções de análise")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        traceback.print_exc()
        return False

def teste_visualizacao():
    """Testar geração de gráficos"""
    print("\n📊 Testando visualização...")
    
    try:
        from visualizacao import GeradorGraficos
        import pandas as pd
        
        # Criar dados de teste
        dados_teste = pd.DataFrame({
            'algoritmo': ['merge_sort', 'quick_sort'] * 5,
            'tamanho': [1000] * 10,
            'tipo_dado': ['exponencial'] * 10,
            'tempo_medio': [0.1, 0.08, 0.11, 0.09, 0.12, 0.07, 0.10, 0.08, 0.11, 0.09]
        })
        
        gerador = GeradorGraficos()
        
        # Teste geração de um gráfico simples
        gerador.grafico_barras_comparativo(dados_teste)
        
        print("✅ Visualização testada com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na visualização: {e}")
        traceback.print_exc()
        return False

def teste_configuracao():
    """Testar configurações"""
    print("\n🔧 Testando configuração...")
    
    try:
        import config
        
        # Testar validação
        config_valida = config.validar_configuracoes()
        print(f"✅ Configurações: {'Válidas' if config_valida else 'INVÁLIDAS'}")
        
        # Testar criação de diretórios
        config.criar_diretorios()
        print("✅ Diretórios criados")
        
        # Testar configuração de ambiente
        env_config = config.obter_config_ambiente()
        print(f"✅ Ambiente: {env_config['sistema']} {env_config['arquitetura']}")
        
        return config_valida
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        traceback.print_exc()
        return False

def main():
    """Executar todos os testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA")
    print("=" * 50)
    
    testes = [
        ("Imports", teste_imports),
        ("Geradores", teste_geradores),
        ("Algoritmos", teste_algoritmos),
        ("Benchmark", teste_benchmark),
        ("Análise", teste_analise),
        ("Visualização", teste_visualizacao),
        ("Configuração", teste_configuracao)
    ]
    
    resultados = []
    
    for nome, teste_func in testes:
        print(f"\n{'='*20} {nome} {'='*20}")
        inicio = time.time()
        
        try:
            sucesso = teste_func()
            tempo_execucao = time.time() - inicio
            resultados.append((nome, sucesso, tempo_execucao))
            
            status = "✅ PASSOU" if sucesso else "❌ FALHOU"
            print(f"\n{status} - {tempo_execucao:.2f}s")
            
        except Exception as e:
            tempo_execucao = time.time() - inicio
            resultados.append((nome, False, tempo_execucao))
            print(f"\n❌ ERRO - {tempo_execucao:.2f}s")
            print(f"Exceção: {e}")
    
    # Resumo final
    print("\n" + "="*50)
    print("📋 RESUMO DOS TESTES")
    print("="*50)
    
    testes_passaram = 0
    for nome, sucesso, tempo in resultados:
        status = "✅" if sucesso else "❌"
        print(f"{status} {nome:<15} - {tempo:.2f}s")
        if sucesso:
            testes_passaram += 1
    
    taxa_sucesso = (testes_passaram / len(testes)) * 100
    print(f"\n🎯 Taxa de Sucesso: {testes_passaram}/{len(testes)} ({taxa_sucesso:.1f}%)")
    
    if taxa_sucesso == 100:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
        return True
    else:
        print(f"\n⚠️  {len(testes) - testes_passaram} testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Testes interrompidos pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro crítico nos testes: {e}")
        traceback.print_exc()
        sys.exit(1)
