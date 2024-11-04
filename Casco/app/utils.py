def validate_password(password):
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    if all(ch == password[0] for ch in password):
        return False, "A senha não pode ser composta pelo mesmo caractere repetido."
    return True, "Senha válida."
