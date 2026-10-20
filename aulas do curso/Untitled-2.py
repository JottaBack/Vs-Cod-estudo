try:
    altura = float(input("Digite sua altura em metros (ex.: 1.70): "))

    if altura <= 0:
        raise ValueError("A altura precisa ser maior que zero.")

    peso_minimo = 18.5 * altura**2
    peso_maximo = 24.9 * altura**2
    peso_referencia = 22 * altura**2

    print(f"\nFaixa de peso saudável estimada: {peso_minimo:.1f} kg a {peso_maximo:.1f} kg")
    print(f"Peso de referência estimado: {peso_referencia:.1f} kg")
    print("\nEstimativa baseada em IMC para adultos; não substitui orientação profissional.")
except ValueError as erro:
    print(f"Entrada inválida: {erro}")
