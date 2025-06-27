"""
Teste de sintaxe simples para validar se o código compila corretamente
"""

import ast
import sys
import os

def test_syntax(file_path):
    """Testar se um arquivo Python tem sintaxe válida"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compilar o código para verificar sintaxe
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Erro de sintaxe: {e}"
    except Exception as e:
        return False, f"Erro: {e}"

def main():
    """Executar testes de sintaxe"""
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    # Arquivos para testar
    files_to_test = [
        'analise.py',
        'benchmark.py',
        'algoritmos.py',
        'geradores.py',
        'visualizacao.py',
        'utils.py',
        'config.py',
        'main.py'
    ]
    
    print("🔍 Testando sintaxe dos arquivos Python...")
    print("=" * 50)
    
    all_passed = True
    
    for filename in files_to_test:
        file_path = os.path.join(src_dir, filename)
        if os.path.exists(file_path):
            success, error = test_syntax(file_path)
            if success:
                print(f"✓ {filename}: Sintaxe válida")
            else:
                print(f"❌ {filename}: {error}")
                all_passed = False
        else:
            print(f"⚠️ {filename}: Arquivo não encontrado")
    
    print("=" * 50)
    if all_passed:
        print("🎉 Todos os arquivos passaram no teste de sintaxe!")
        print("📋 Próximos passos:")
        print("   1. Execute 'run.bat setup' para configurar o Docker")
        print("   2. Execute 'run.bat test' para executar os testes")
        print("   3. Execute 'run.bat run' para executar o experimento")
    else:
        print("❌ Alguns arquivos têm problemas de sintaxe")
        sys.exit(1)

if __name__ == "__main__":
    main()
