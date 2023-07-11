def instalarLibrerias():
    import os
    print("Iniciando proceso de instalacion automatizada de librerias. Esta operacion se realiza una sola vez. Por favor espere, puede tardar unos minutos...")
    try:
        try:
            os.system("pip install DateTime")
            print("Libreria DateTime instalada...")
        except:
            pass
        try:
            os.system("pip install selenium")
            print("Libreria Selenium instalada...")
        except:
            pass
        try:
            os.system("pip install chromedriver-autoinstaller")
            print("Libreria Chromedriver-autoinstaller instalada...")
        except:
            pass    
        try:
            os.system("pip install mysql-connector")
            print("Libreria Mysql-connector instalada...")
        except:
            pass  
        print("Las librerias fueron instaladas automatizadamente con exito.")
    except:
        print("Las librerias no fueron instaladas de forma automatizada. Es posible que ya se encuentren instaladas o existan problemas de compatibilidad.")