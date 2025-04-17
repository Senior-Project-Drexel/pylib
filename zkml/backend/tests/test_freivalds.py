import numpy as np
import pytest
from zkml.backend import Freivalds


class MockClientManager:
    def client(self):
        return self

    async def send_matrix(self, a, b, op):
        return "test_id"

    async def recv_matrix(self, matrix_id):
        return None  # Not used in these tests since we test _verify directly


@pytest.fixture
def freivalds():
    return Freivalds(MockClientManager())


def test_verify_integer_correct():
    """Test verification with correct integer matrix multiplication"""
    f = Freivalds(MockClientManager())
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    C = A @ B  # Correct result
    assert f._verify(A, B, C)


def test_verify_integer_incorrect():
    """Test verification with incorrect integer matrix multiplication"""
    f = Freivalds(MockClientManager())
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    C = A @ B + 1  # Incorrect result
    assert not f._verify(A, B, C)


def test_verify_float_correct():
    """Test verification with correct floating point matrix multiplication"""
    f = Freivalds(MockClientManager())
    A = np.array([[0.1, 0.2], [0.3, 0.4]])
    B = np.array([[0.5, 0.6], [0.7, 0.8]])
    C = A @ B
    assert f._verify(A, B, C)


def test_verify_float_incorrect():
    """Test verification with incorrect floating point matrix multiplication"""
    f = Freivalds(MockClientManager())
    A = np.array([[0.1, 0.2], [0.3, 0.4]])
    B = np.array([[0.5, 0.6], [0.7, 0.8]])
    C = A @ B + 0.00001
    assert not f._verify(A, B, C)


def test_verify_large_matrices():
    """Test verification with larger matrices"""
    f = Freivalds(MockClientManager())
    A = np.random.rand(100, 100)
    B = np.random.rand(100, 100)
    C = A @ B
    assert f._verify(A, B, C)


def test_verify_different_dimensions():
    """Test verification with matrices of different compatible dimensions"""
    f = Freivalds(MockClientManager())
    A = np.random.rand(10, 20)
    B = np.random.rand(20, 5)
    C = A @ B
    assert f._verify(A, B, C)


def test_verify_near_zero():
    """Test verification with very small numbers"""
    f = Freivalds(MockClientManager())
    A = np.array([[1e-10, 2e-10], [3e-10, 4e-10]])
    B = np.array([[5e-10, 6e-10], [7e-10, 8e-10]])
    C = A @ B
    assert f._verify(A, B, C)
