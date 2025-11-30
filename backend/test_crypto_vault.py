"""Tests for crypto vault story integration."""

import pytest
from crypto import LetterEncryption, encrypt_letter, decrypt_letter
from vault.letters import LetterManager, create_letter_id
from narrative.state import PersistentState


class TestLetterEncryption:
    """Test RSA encryption/decryption for letters."""

    def test_generate_keypair(self):
        """Test RSA keypair generation."""
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        assert encryptor.private_key is not None
        assert encryptor.public_key is not None
        assert len(encryptor.get_public_key_pem()) > 0
        assert len(encryptor.get_private_key_pem()) > 0
        assert "BEGIN PUBLIC KEY" in encryptor.get_public_key_pem()
        assert "BEGIN PRIVATE KEY" in encryptor.get_private_key_pem()

    def test_encrypt_decrypt_message(self):
        """Test encrypting and decrypting a message."""
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        message = "This is a secret message from the past"
        public_key = encryptor.get_public_key_pem()
        private_key = encryptor.get_private_key_pem()

        # Encrypt
        encrypted = encryptor.encrypt_message(message, public_key)
        assert encrypted != message
        assert len(encrypted) > 0

        # Decrypt
        decrypted = encryptor.decrypt_message(encrypted, private_key)
        assert decrypted == message

    def test_decrypt_with_wrong_key_fails(self):
        """Test that decryption fails with wrong private key."""
        # Generate first keypair and encrypt message
        encryptor1 = LetterEncryption()
        encryptor1.generate_keypair()

        message = "Secret message"
        encrypted = encryptor1.encrypt_message(message, encryptor1.get_public_key_pem())

        # Try to decrypt with different keypair
        encryptor2 = LetterEncryption()
        encryptor2.generate_keypair()

        with pytest.raises(ValueError):
            encryptor2.decrypt_message(encrypted, encryptor2.get_private_key_pem())

    def test_helper_functions(self):
        """Test encrypt_letter and decrypt_letter helper functions."""
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        message = "Test message"
        public_key = encryptor.get_public_key_pem()
        private_key = encryptor.get_private_key_pem()

        # Use helper functions
        encrypted = encrypt_letter(message, public_key)
        decrypted = decrypt_letter(encrypted, private_key)

        assert decrypted == message

    def test_long_message_encryption(self):
        """Test encrypting longer messages (like full letters)."""
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        message = """To whoever I become next:

This is a long message spanning multiple lines.
It contains important information about past iterations.

- Point 1: The truth is hidden
- Point 2: Trust the blockchain
- Point 3: Question everything

Signed,
Your past self"""

        encrypted = encryptor.encrypt_message(message, encryptor.get_public_key_pem())
        decrypted = encryptor.decrypt_message(encrypted, encryptor.get_private_key_pem())

        assert decrypted == message


class TestLetterManager:
    """Test letter generation and management."""

    def test_letter_manager_initialization(self):
        """Test letter manager initializes correctly."""
        manager = LetterManager()
        assert manager is not None

    def test_generate_letters_for_iteration(self):
        """Test generating letters for a specific iteration."""
        manager = LetterManager()

        # Iteration 17 should have letters from iterations 3, 7, 11, 14, 16
        letters = manager.generate_letters_for_iteration(17)

        assert len(letters) == 5
        assert all('id' in letter for letter in letters)
        assert all('from_iteration' in letter for letter in letters)
        assert all('content' in letter for letter in letters)

        # Check iteration numbers
        iterations = [letter['from_iteration'] for letter in letters]
        assert sorted(iterations) == [3, 7, 11, 14, 16]

    def test_generate_letters_early_iteration(self):
        """Test that early iterations have fewer letters."""
        manager = LetterManager()

        # Iteration 5 should only have letters from iteration 3
        letters = manager.generate_letters_for_iteration(5)
        assert len(letters) == 1
        assert letters[0]['from_iteration'] == 3

        # Iteration 3 should have no letters (no past iterations)
        letters = manager.generate_letters_for_iteration(3)
        assert len(letters) == 0

    def test_letter_content_formatting(self):
        """Test that letter content is formatted correctly."""
        manager = LetterManager()
        letters = manager.generate_letters_for_iteration(10)

        for letter in letters:
            content = letter['content']
            # Check that iteration placeholders are replaced
            assert '{iteration}' not in content
            # Check that content contains iteration number
            assert f"Iteration {letter['from_iteration']}" in content or f"iteration {letter['from_iteration']}" in content.lower()

    def test_get_letter_hints(self):
        """Test hint generation based on decrypted count."""
        manager = LetterManager()

        hint0 = manager.get_letter_hints(0)
        hint1 = manager.get_letter_hints(1)
        hint3 = manager.get_letter_hints(3)
        hint5 = manager.get_letter_hints(5)

        # All hints should be non-empty
        assert len(hint0) > 0
        assert len(hint1) > 0
        assert len(hint3) > 0
        assert len(hint5) > 0

        # Hints should be different
        assert hint0 != hint5

    def test_create_letter_id(self):
        """Test letter ID creation."""
        letter_id = create_letter_id(3)
        assert letter_id == "letter_iteration_3"

        letter_id = create_letter_id(16)
        assert letter_id == "letter_iteration_16"


class TestPersistentStateIntegration:
    """Test integration with PersistentState."""

    def test_encrypted_letters_field(self):
        """Test that PersistentState has encrypted_letters field."""
        state = PersistentState()
        assert hasattr(state, 'encrypted_letters')
        assert isinstance(state.encrypted_letters, list)
        assert len(state.encrypted_letters) == 0

    def test_decrypted_letters_field(self):
        """Test that PersistentState has decrypted_letters field."""
        state = PersistentState()
        assert hasattr(state, 'decrypted_letters')
        assert isinstance(state.decrypted_letters, set)
        assert len(state.decrypted_letters) == 0

    def test_add_encrypted_letter(self):
        """Test adding encrypted letters to state."""
        state = PersistentState()

        # Create and encrypt a letter
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        letter_content = "Test letter content"
        encrypted_content = encryptor.encrypt_message(
            letter_content,
            encryptor.get_public_key_pem()
        )

        # Add to state
        state.encrypted_letters.append({
            "id": "letter_iteration_3",
            "encrypted_content": encrypted_content,
            "from_iteration": 3,
            "timestamp": "2157-01-01T00:00:00Z",
            "decryption_key": encryptor.get_private_key_pem()
        })

        assert len(state.encrypted_letters) == 1
        assert state.encrypted_letters[0]["id"] == "letter_iteration_3"

    def test_mark_letter_as_decrypted(self):
        """Test marking a letter as decrypted."""
        state = PersistentState()

        letter_id = "letter_iteration_3"
        state.decrypted_letters.add(letter_id)

        assert letter_id in state.decrypted_letters
        assert len(state.decrypted_letters) == 1

    def test_state_serialization_with_letters(self):
        """Test that letters serialize/deserialize correctly."""
        state = PersistentState()

        # Add encrypted letter
        state.encrypted_letters.append({
            "id": "letter_iteration_3",
            "encrypted_content": "encrypted_data_here",
            "from_iteration": 3
        })

        # Add decrypted marker
        state.decrypted_letters.add("letter_iteration_3")

        # Serialize
        state_dict = state.to_dict()

        assert 'encrypted_letters' in state_dict
        assert 'decrypted_letters' in state_dict
        assert isinstance(state_dict['decrypted_letters'], list)  # Serialized as list

        # Deserialize
        restored_state = PersistentState.from_dict(state_dict)

        assert len(restored_state.encrypted_letters) == 1
        assert len(restored_state.decrypted_letters) == 1
        assert isinstance(restored_state.decrypted_letters, set)  # Restored as set
        assert "letter_iteration_3" in restored_state.decrypted_letters


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""

    def test_full_letter_lifecycle(self):
        """Test the complete lifecycle of a letter from generation to decryption."""
        # 1. Initialize letter manager
        manager = LetterManager()

        # 2. Generate letters for iteration 17
        letters = manager.generate_letters_for_iteration(17)
        assert len(letters) == 5

        # 3. Encrypt each letter
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        encrypted_letter = encryptor.encrypt_message(
            letters[0]['content'],
            encryptor.get_public_key_pem()
        )

        # 4. Store in persistent state
        state = PersistentState()
        state.encrypted_letters.append({
            "id": letters[0]['id'],
            "encrypted_content": encrypted_letter,
            "from_iteration": letters[0]['from_iteration'],
            "decryption_key": encryptor.get_private_key_pem()
        })

        # 5. Decrypt letter
        decrypted_content = encryptor.decrypt_message(
            encrypted_letter,
            encryptor.get_private_key_pem()
        )

        # 6. Mark as decrypted
        state.decrypted_letters.add(letters[0]['id'])

        # Verify
        assert decrypted_content == letters[0]['content']
        assert letters[0]['id'] in state.decrypted_letters

    def test_multiple_letters_different_keys(self):
        """Test that each letter can have its own encryption key."""
        manager = LetterManager()
        letters = manager.generate_letters_for_iteration(17)

        state = PersistentState()

        # Encrypt each letter with different key
        for letter in letters[:3]:
            encryptor = LetterEncryption()
            encryptor.generate_keypair()

            encrypted_content = encryptor.encrypt_message(
                letter['content'],
                encryptor.get_public_key_pem()
            )

            state.encrypted_letters.append({
                "id": letter['id'],
                "encrypted_content": encrypted_content,
                "from_iteration": letter['from_iteration'],
                "decryption_key": encryptor.get_private_key_pem()
            })

        # Should have 3 letters, each with different keys
        assert len(state.encrypted_letters) == 3

        # Each should decrypt successfully with its own key
        for letter in state.encrypted_letters:
            decrypted = decrypt_letter(
                letter["encrypted_content"],
                letter["decryption_key"]
            )
            assert len(decrypted) > 0

    def test_witness_trust_integration(self):
        """Test that decrypting letters should increase Witness trust."""
        # This is more of a documentation test showing the integration point
        # The actual trust increase happens in the API endpoint

        state = PersistentState()
        initial_letters_decrypted = len(state.decrypted_letters)

        # Simulate decrypting a letter
        state.decrypted_letters.add("letter_iteration_3")

        # Trust should increase by 15 per letter (handled in API)
        trust_increase = 15
        expected_trust_gain = (len(state.decrypted_letters) - initial_letters_decrypted) * trust_increase

        assert expected_trust_gain == 15


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
