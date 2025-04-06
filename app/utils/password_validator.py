import re
from typing import Tuple, List

class PasswordValidator:
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_numbers = True
        self.require_special_chars = True

    def validate(self, password: str) -> Tuple[bool, List[str]]:
        """
        Valida se a senha atende aos requisitos mínimos de segurança.
        
        Args:
            password (str): A senha a ser validada
            
        Returns:
            bool: True se a senha atende aos requisitos, False caso contrário
        """
        errors = []

        if len(password) < self.min_length:
            errors.append(f"A senha deve ter pelo menos {self.min_length} caracteres")

        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("A senha deve conter pelo menos uma letra maiúscula")

        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("A senha deve conter pelo menos uma letra minúscula")

        if self.require_numbers and not re.search(r'[0-9]', password):
            errors.append("A senha deve conter pelo menos um número")

        if self.require_special_chars and not re.search(r'[^A-Za-z0-9]', password):
            errors.append("A senha deve conter pelo menos um caractere especial")

        return len(errors) == 0, errors

    def get_requirements(self):
        """
        Retorna uma lista com os requisitos mínimos de segurança.
        
        Returns:
            list: Lista com os requisitos mínimos de segurança
        """
        requirements = [
            f'Mínimo de {self.min_length} caracteres'
        ]

        if self.require_uppercase:
            requirements.append('Pelo menos uma letra maiúscula')

        if self.require_lowercase:
            requirements.append('Pelo menos uma letra minúscula')

        if self.require_numbers:
            requirements.append('Pelo menos um número')

        if self.require_special_chars:
            requirements.append('Pelo menos um caractere especial')

        return requirements

    def get_password_strength(self, password: str) -> int:
        """
        Retorna a força da senha em uma escala de 0 a 4:
        0: Muito fraca
        1: Fraca
        2: Média
        3: Forte
        4: Muito forte
        """
        score = 0

        # Comprimento
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1

        # Caracteres maiúsculos
        if re.search(r'[A-Z]', password):
            score += 1

        # Caracteres minúsculos
        if re.search(r'[a-z]', password):
            score += 1

        # Números
        if re.search(r'[0-9]', password):
            score += 1

        # Caracteres especiais
        if re.search(r'[^A-Za-z0-9]', password):
            score += 1

        # Normaliza o score para a escala de 0 a 4
        return min(4, score // 2) 