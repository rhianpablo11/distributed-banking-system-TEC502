def mascarar_cpf(cpf):
    # Verifica se o CPF está no formato correto
    if len(cpf) == 14 and cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-':
        # Substitui os três primeiros dígitos e os dois últimos por asteriscos
        cpf_mascarado = '***.' + cpf[4:7] + '.' + cpf[8:11] + '-**'
        return cpf_mascarado
    else:
        raise ValueError("CPF no formato incorreto. Use o formato XXX.XXX.XXX-XX")
    
# Exemplo de uso
cpf = '111.111.111-14735341'
cpf_mascarado = mascarar_cpf(cpf)
print(cpf_mascarado)  # Saída: ***.111.111-**
