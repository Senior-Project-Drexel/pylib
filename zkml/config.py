class Config:
    def __init__(self):
        self.backend = "trust"  # {"local", "trust", "freivalds"}
        self.client_manager = "roundrobin"
        self.verifier = "noop"
        self.addresses = []
        self._backend_instance = None
        self._verifier_instance = None
        self._client_manager_instance = None

    def configure(
        self,
        addresses=None,
        backend=None,
        verifier=None,
        client_manager=None,
        **backend_options,
    ):
        if addresses is not None:
            self.addresses = addresses
        if backend is not None:
            self.backend = backend
            self._backend_instance = None
        if verifier is not None:
            self.verifier = verifier
            self._verifier_instance = None
        if client_manager is not None:
            self.client_manager = client_manager
            self._client_manager_instance = None

    def backend_instance(self):
        if self._backend_instance is None:
            self._backend_instance = self._initialize_backend()
        return self._backend_instance

    def verifier_instance(self):
        if self._verifier_instance is None:
            self._verifier_instance = self._initialize_verifier()
        return self._verifier_instance

    def client_manager_instance(self):
        if self._client_manager_instance is None:
            self._client_manager_instance = self._initialize_client_manager()
        return self._client_manager_instance

    def _initialize_backend(self):
        if self.backend == "local":
            from .backend.local import Local

            return Local()
        if self.backend == "trust":
            from .backend.remote_trust import RemoteTrust

            if not self.addresses:
                raise ValueError("No server addresses configured")
            return RemoteTrust()
        if self.backend == "freivalds":
            from .backend.remote_freivalds import RemoteFreivalds

            if not self.addresses:
                raise ValueError("No server addresses configured")
            return RemoteFreivalds()
        else:
            raise ValueError(
                "Unknown backend. Backend options: local, trust, freivalds"
            )

    def _initialize_verifier(self):
        if self.verifier == "noop":
            from .verifier import NopVerifier

            return NopVerifier()
        else:
            raise ValueError("Unknown verifier")

    def _initialize_client_manager(self):
        if self.client_manager == "roundrobin":
            from .client_manager import RoundRobinClientManager

            return RoundRobinClientManager(self.addresses)
        else:
            raise ValueError("Unknown client manager")
