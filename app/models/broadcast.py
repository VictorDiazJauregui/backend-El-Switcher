class Broadcast:
    _instance = None
    _sids = {}

    # Singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Broadcast, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add_sid(self, player_id, sid):
        self._sids[player_id] = sid

    def get_sid(self, player_id):
        return self._sids.get(player_id)

    def exists_sid(self, player_id):
        return player_id in self._sids

    def remove_sid(self, player_id):
        if player_id in self._sids:
            del self._sids[player_id]

    async def register_player_socket(self, sio, player_id, game_id, sid):
        self.add_sid(player_id, sid)
        await sio.enter_room(sid, str(game_id))

    async def unregister_player_socket(self, sio, player_id, game_id):
        await sio.leave_room(self.get_sid(player_id), str(game_id))
        self.remove_sid(player_id)

    async def broadcast(self, sio, game_id, event, data):
        await sio.emit(event, data, room=str(game_id))

    async def send_to_player(self, sio, player_id, event, data):
        sid = self.get_sid(player_id)

        if not sid:
            return

        await sio.emit(event, data, room=sid)
