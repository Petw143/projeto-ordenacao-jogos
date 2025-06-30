import numpy as np
import random
from typing import List
import logging

class GeradorDados:
    """Classe para gerar diferentes tipos de dados de teste"""
    
    def __init__(self, seed=42):
        """Inicializar com seed para reprodutibilidade"""
        np.random.seed(seed)
        random.seed(seed)
        self.lambda_exp = 0.001  # Taxa da distribuição exponencial
        self.escala_max = 10000  # Pontuação máxima
        
    def gerar(self, tamanho: int, tipo: str) -> List[int]:
        """
        Gerar dados conforme especificado
        
        Args:
            tamanho: Número de elementos
            tipo: 'exponencial' ou 'quase_ordenado'
        
        Returns:
            Lista com os dados gerados
        """
        if tipo == 'exponencial':
            return self._gerar_exponencial(tamanho)
        elif tipo == 'quase_ordenado':
            return self._gerar_quase_ordenado(tamanho)
        else:
            raise ValueError(f"Tipo '{tipo}' não reconhecido")
    
    def _gerar_exponencial(self, tamanho: int) -> List[int]:
        """
        Gerar pontuações com distribuição exponencial usando método da transformação inversa
        
        Justificativa: Em jogos online, poucos jogadores têm pontuações muito altas,
        enquanto a maioria tem pontuações baixas/médias.
        
        MÉTODO DA TRANSFORMAÇÃO INVERSA:
        1. Gerar números aleatórios U ~ Uniforme(0,1)
        2. Aplicar função inversa da CDF exponencial
        3. Função inversa: F^(-1)(u) = -ln(1-u)/λ
        4. Se U ~ Uniforme(0,1), então X = -ln(1-U)/λ ~ Exponencial(λ)
        
        DERIVAÇÃO:
        - CDF da exponencial: F(x) = 1 - e^(-λx)
        - Igualando F(x) = u: u = 1 - e^(-λx)
        - Resolvendo para x: e^(-λx) = 1 - u
        - Aplicando ln: -λx = ln(1 - u)
        - Função inversa: x = -ln(1 - u)/λ
        """
        logging.info(f"Gerando {tamanho} pontuações com distribuição exponencial via transformação inversa")
        
        # ETAPA 1: Gerar números uniformes como base
        uniformes = np.random.uniform(0, 1, tamanho)
        logging.debug(f"Gerados {tamanho} números uniformes: min={uniformes.min():.3f}, max={uniformes.max():.3f}")
        
        # ETAPA 2: Aplicar transformação inversa para distribuição exponencial
        # X = -ln(1-U)/λ onde U ~ Uniform(0,1)
        exponenciais = -np.log(1 - uniformes) / self.lambda_exp
        logging.debug(f"Aplicada transformação inversa: min={exponenciais.min():.1f}, max={exponenciais.max():.1f}")
        
        # ETAPA 3: Escalar para faixa de pontuações de jogo (0 a escala_max)
        pontuacoes = np.clip(exponenciais, 0, self.escala_max).astype(int)
        
        # ETAPA 4: Embaralhar para remover qualquer ordem residual
        np.random.shuffle(pontuacoes)
        
        logging.info(f"Distribuição exponencial gerada - Min: {min(pontuacoes)}, Max: {max(pontuacoes)}, Média: {np.mean(pontuacoes):.1f}")
        
        return pontuacoes.tolist()
    
    def _gerar_quase_ordenado(self, tamanho: int) -> List[int]:
        """
        Gerar dados quase ordenados usando base uniforme com perturbações precisas
        
        Justificativa: Simula ranking de jogadores que é atualizado frequentemente,
        onde a maioria mantém posições próximas, mas alguns jogadores mudam drasticamente.
        
        MÉTODO DA CONVERSÃO DE DISTRIBUIÇÃO UNIFORME:
        1. Criar sequência ordenada base [1, 2, 3, ..., tamanho]
        2. Gerar números aleatórios U ~ Uniforme(0,1) para seleção de posições
        3. Selecionar exatamente 10% das posições
        4. Para cada posição selecionada, usar uniforme para gerar novo valor aleatório
        
        DERIVAÇÃO DA TRANSFORMAÇÃO:
        - Base: Sequência ordenada [1, 2, 3, ..., n]
        - Seleção: 10% das posições escolhidas aleatoriamente
        - Novo valor: U ~ Uniforme(0,1) → valor ∈ [1, tamanho]
        - Resultado: exatamente 10% de elementos fora de ordem
        """
        logging.info(f"Gerando {tamanho} pontuações quase ordenadas com 10% de perturbação precisa")
        
        # ETAPA 1: Criar sequência ordenada base (simula ranking estável)
        dados_ordenados = list(range(1, tamanho + 1))
        logging.debug(f"Criada sequência ordenada: [1, 2, 3, ..., {tamanho}]")
        
        # ETAPA 2: Calcular número exato de perturbações (10%)
        num_perturbacoes = max(1, int(tamanho * 0.1))
        
        # ETAPA 3: Gerar números uniformes para seleção de posições e novos valores
        uniformes_posicoes = np.random.uniform(0, 1, tamanho)
        uniformes_valores = np.random.uniform(0, 1, num_perturbacoes)
        
        # ETAPA 4: Selecionar posições aleatórias para perturbar
        posicoes_perturbacao = random.sample(range(tamanho), num_perturbacoes)
        posicoes_perturbacao.sort()  # ordenar para logging
        
        # ETAPA 5: Aplicar perturbações usando números uniformes
        valores_originais = []
        valores_novos = []
        
        for idx, pos in enumerate(posicoes_perturbacao):
            # Salvar valor original
            valor_original = dados_ordenados[pos]
            valores_originais.append(valor_original)
            
            # Usar número uniforme para gerar novo valor completamente aleatório
            u = uniformes_valores[idx]
            novo_valor = int(1 + u * (tamanho - 1))  # Converter U[0,1] → [1, tamanho]
            valores_novos.append(novo_valor)
            
            # Substituir valor
            dados_ordenados[pos] = novo_valor
            
            logging.debug(f"Perturbação {idx+1}: posição {pos}, {valor_original} → {novo_valor} (U={u:.3f})")
        
        # ETAPA 6: Verificação e logging do resultado
        logging.info(f"Dados quase ordenados gerados:")
        logging.info(f"  - {num_perturbacoes} perturbações ({num_perturbacoes/tamanho*100:.1f}%)")
        logging.info(f"  - Posições perturbadas: {posicoes_perturbacao}")
        logging.info(f"  - Valores originais: {valores_originais}")
        logging.info(f"  - Novos valores: {valores_novos}")
        
        return dados_ordenados