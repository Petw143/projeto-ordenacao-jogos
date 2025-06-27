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
        Gerar pontuações com distribuição exponencial
        
        Justificativa: Em jogos online, poucos jogadores têm pontuações muito altas,
        enquanto a maioria tem pontuações baixas/médias.
        
        Método: Transformação inversa
        Se U ~ Uniforme(0,1), então X = -ln(1-U)/λ ~ Exponencial(λ)
        """
        logging.info(f"Gerando {tamanho} pontuações com distribuição exponencial")
        
        # Gerar números uniformes
        uniformes = np.random.uniform(0, 1, tamanho)
        
        # Aplicar transformação inversa para distribuição exponencial
        exponenciais = -np.log(1 - uniformes) / self.lambda_exp
        
        # Escalar para faixa de pontuações de jogo (0 a escala_max)
        pontuacoes = np.clip(exponenciais, 0, self.escala_max).astype(int)
        
        # Embaralhar para remover qualquer ordem residual
        np.random.shuffle(pontuacoes)
        
        logging.info(f"Distribuição gerada - Min: {min(pontuacoes)}, Max: {max(pontuacoes)}, Média: {np.mean(pontuacoes):.1f}")
        
        return pontuacoes.tolist()
    
    def _gerar_quase_ordenado(self, tamanho: int) -> List[int]:
        """
        Gerar dados quase ordenados (90% ordenado + 10% perturbação)
        
        Justificativa: Simula ranking de jogadores que é atualizado frequentemente,
        onde a maioria mantém posições próximas, mas alguns jogadores mudam drasticamente.
        """
        logging.info(f"Gerando {tamanho} pontuações quase ordenadas")
        
        # Gerar dados ordenados (simula ranking estável)
        dados_ordenados = list(range(1, tamanho + 1))
        
        # Calcular número de elementos para perturbar (10%)
        num_perturbacoes = int(tamanho * 0.1)
        
        # Selecionar posições aleatórias para perturbar
        posicoes_perturbacao = random.sample(range(tamanho), num_perturbacoes)
        
        # Aplicar perturbações (trocar elementos de posição)
        for i in posicoes_perturbacao:
            # Escolher nova posição aleatória
            j = random.randint(0, tamanho - 1)
            # Trocar elementos
            dados_ordenados[i], dados_ordenados[j] = dados_ordenados[j], dados_ordenados[i]
        
        logging.info(f"Dados quase ordenados gerados com {num_perturbacoes} perturbações")
        
        return dados_ordenados