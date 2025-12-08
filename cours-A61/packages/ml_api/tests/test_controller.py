## test_controller.py ##
def test_root_endpoint_returns_ok(client):
    
    ## Test que l'endpoint racine (/) fonctionne correctement.
    
    ## Vérifie que :
    ## 1. L'API répond avec un code HTTP 200 (succès)
    ## 2. Le contenu de la réponse est bien "ok" comme attendu
    
    # Simulation d'une requête GET sur l'URL racine
    response = client.get("/")
    
    # Vérification du code de statut HTTP
    assert response.status_code == 200
    
    # Vérification du contenu de la réponse
    # On décode les bytes en texte pour la comparaison
    assert response.data.decode("utf-8") == "ok"