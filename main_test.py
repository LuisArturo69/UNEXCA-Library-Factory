from src.factory.resources import resource_factory

def main():
    # Usamos la fábrica para crear los diferentes recursos
    resource1 = resource_factory.crear_recurso('book', titulo="El Quijote", autor="Cervantes")
    resource2 = resource_factory.crear_recurso('laptop', marca="Dell XPS", ram="16GB")
    resource3 = resource_factory.crear_recurso('tablet', modelo="iPad Pro")
    
    # Comprobamos que cada objeto es del tipo correcto y ejecuta su propio método
    resources = [resource1, resource2, resource3]
    
    for resource in resources:
        print(resource.use())
        print(f"Tipo de objeto: {type(resource).__name__}\n")

if __name__ == "__main__":
    main()
