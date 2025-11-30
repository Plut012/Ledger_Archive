"""Integration tests for blockchain API endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestBlockchainAPI:
    """Test blockchain API endpoints."""

    def test_get_block_by_index(self, client):
        """Should retrieve block by index."""
        response = client.get("/api/blockchain/block/100")

        assert response.status_code == 200
        data = response.json()

        assert data["index"] == 100
        assert "hash" in data
        assert "transactions" in data
        assert "previous_hash" in data
        assert "timestamp" in data
        assert "nonce" in data
        assert isinstance(data["isGraveyard"], bool)
        assert data["isGraveyard"] == False  # Block 100 is not in graveyard

    def test_get_graveyard_block(self, client):
        """Should identify graveyard blocks."""
        response = client.get("/api/blockchain/block/55000")

        assert response.status_code == 200
        data = response.json()

        assert data["index"] == 55000
        assert data["isGraveyard"] == True

    def test_get_story_block(self, client):
        """Should retrieve story-critical blocks."""
        # Block 127445 is Witness first contact
        response = client.get("/api/blockchain/block/127445")

        assert response.status_code == 200
        data = response.json()

        assert data["index"] == 127445
        assert len(data["transactions"]) == 1
        assert data["transactions"][0]["memo"] == "V2l0bmVzcyBsaXZlcw=="
        assert data["transactions"][0]["sender"] == "NODE-UNKNOWN"

    def test_deterministic_generation_via_api(self, client):
        """Same block should return same data on multiple calls."""
        response1 = client.get("/api/blockchain/block/1000")
        response2 = client.get("/api/blockchain/block/1000")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        assert data1["hash"] == data2["hash"]
        assert data1["nonce"] == data2["nonce"]
        assert len(data1["transactions"]) == len(data2["transactions"])

    def test_reconstruct_consciousness_endpoint(self, client):
        """Should reconstruct consciousness from archive block."""
        # Block 74221 has Administrator Chen's testimony
        response = client.post(
            "/api/blockchain/reconstruct",
            json={
                "blockIndex": 74221,
                "txIndex": 0,
                "playerId": "test_player"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["blockIndex"] == 74221
        assert data["subject"] == "Administrator Chen"
        assert data["status"] == "TRANSCENDED"
        assert "reconstruction" in data
        assert "CONSCIOUSNESS RECONSTRUCTION PROTOCOL" in data["reconstruction"]

        # Should include state updates
        assert "stateUpdates" in data
        assert data["stateUpdates"]["archivistSuspicion"] == 20
        assert data["stateUpdates"]["witnessTrust"] == 10

    def test_reconstruct_invalid_tx_index(self, client):
        """Should return error for invalid transaction index."""
        response = client.post(
            "/api/blockchain/reconstruct",
            json={
                "blockIndex": 74221,
                "txIndex": 999,
                "playerId": "test_player"
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_reconstruct_non_archive_transaction(self, client):
        """Should return error for non-archive transactions."""
        response = client.post(
            "/api/blockchain/reconstruct",
            json={
                "blockIndex": 1000,
                "txIndex": 0,
                "playerId": "test_player"
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_reconstruct_missing_block_index(self, client):
        """Should return error when blockIndex is missing."""
        response = client.post(
            "/api/blockchain/reconstruct",
            json={
                "txIndex": 0,
                "playerId": "test_player"
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_state_updates_accumulate(self, client):
        """State should accumulate across multiple reconstructions."""
        player_id = "test_player_accumulate"

        # First reconstruction
        response1 = client.post(
            "/api/blockchain/reconstruct",
            json={
                "blockIndex": 74221,
                "txIndex": 0,
                "playerId": player_id
            }
        )

        data1 = response1.json()
        assert data1["stateUpdates"]["archivistSuspicion"] == 20
        assert data1["stateUpdates"]["witnessTrust"] == 10

        # Second reconstruction (same player)
        # Find another archive block in graveyard
        response2 = client.post(
            "/api/blockchain/reconstruct",
            json={
                "blockIndex": 65432,  # Another story block with archive tx
                "txIndex": 0,
                "playerId": player_id
            }
        )

        data2 = response2.json()
        # Should accumulate: 20 + 20 = 40, 10 + 10 = 20
        assert data2["stateUpdates"]["archivistSuspicion"] == 40
        assert data2["stateUpdates"]["witnessTrust"] == 20


class TestBlockchainEdgeCases:
    """Test edge cases for blockchain API."""

    def test_large_block_index(self, client):
        """Should handle large block indices."""
        response = client.get("/api/blockchain/block/849999")

        assert response.status_code == 200
        data = response.json()
        assert data["index"] == 849999

    def test_genesis_block(self, client):
        """Should handle block 0 (genesis)."""
        response = client.get("/api/blockchain/block/0")

        assert response.status_code == 200
        data = response.json()
        assert data["index"] == 0
        assert data["previous_hash"] == "0" * 64

    def test_graveyard_boundaries(self, client):
        """Should correctly identify graveyard boundaries."""
        # Just before graveyard
        response1 = client.get("/api/blockchain/block/49999")
        assert response1.json()["isGraveyard"] == False

        # Graveyard start
        response2 = client.get("/api/blockchain/block/50000")
        assert response2.json()["isGraveyard"] == True

        # Graveyard end
        response3 = client.get("/api/blockchain/block/75000")
        assert response3.json()["isGraveyard"] == True

        # Just after graveyard
        response4 = client.get("/api/blockchain/block/75001")
        assert response4.json()["isGraveyard"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
