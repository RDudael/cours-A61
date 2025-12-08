##  tests/conftest.py ##
import pytest
from api.app import app as flask_app


@pytest.fixture
def app():
    
    ## Fixture Pytest qui fournit une instance configurée pour les tests.
    
    ## Configure l'application Flask en mode TESTING et la rend disponible
    ## à toutes les fonctions de test qui la demandent en paramètre.
    
    # Activation du mode TESTING de Flask
    # Cela désactive certaines fonctionnalités comme la capture d'erreurs
    # et rend les tests plus prévisibles
    flask_app.config.update({"TESTING": True})
    
    # 'yield' rend l'application disponible pour les tests
    # et garantit un nettoyage après chaque test
    yield flask_app


@pytest.fixture
def client(app):
    
    ## Fixture qui crée un client de test pour simuler des requêtes HTTP.
    
    ## Ce client permet de tester les endpoints API sans avoir à démarrer
    ## un serveur réel. C'est plus rapide et plus isolé.
    
    return app.test_client()