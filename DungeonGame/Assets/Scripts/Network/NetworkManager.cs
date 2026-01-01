using UnityEngine;
using Photon.Pun;
using Photon.Realtime;

namespace DarkDungeon.Network
{
    /// <summary>
    /// Главный менеджер сети. Управляет подключением к Photon и комнатами.
    /// </summary>
    public class NetworkManager : MonoBehaviourPunCallbacks
    {
        public static NetworkManager Instance { get; private set; }

        [Header("Настройки Photon")]
        [SerializeField] private string gameVersion = "0.1";
        [SerializeField] private byte maxPlayersPerRoom = 4; // Пока 4, можно увеличить

        [Header("Статус")]
        [SerializeField] private bool autoConnect = true;

        private void Awake()
        {
            // Singleton паттерн - только один NetworkManager
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);

            // Важно! Синхронизируем сцены между игроками
            PhotonNetwork.AutomaticallySyncScene = true;
        }

        private void Start()
        {
            if (autoConnect && !PhotonNetwork.IsConnected)
            {
                ConnectToPhoton();
            }
        }

        /// <summary>
        /// Подключается к Photon Cloud
        /// </summary>
        public void ConnectToPhoton()
        {
            Debug.Log("Подключаемся к Photon...");
            PhotonNetwork.GameVersion = gameVersion;
            PhotonNetwork.ConnectUsingSettings();
        }

        /// <summary>
        /// Создает новую комнату
        /// </summary>
        public void CreateRoom(string roomName = null)
        {
            if (!PhotonNetwork.IsConnected)
            {
                Debug.LogError("Не подключены к Photon!");
                return;
            }

            RoomOptions roomOptions = new RoomOptions
            {
                MaxPlayers = maxPlayersPerRoom,
                IsVisible = true,
                IsOpen = true
            };

            // Если имя не указано, Photon создаст случайное
            if (string.IsNullOrEmpty(roomName))
            {
                PhotonNetwork.CreateRoom(null, roomOptions);
            }
            else
            {
                PhotonNetwork.CreateRoom(roomName, roomOptions);
            }
        }

        /// <summary>
        /// Присоединяется к случайной комнате
        /// </summary>
        public void JoinRandomRoom()
        {
            if (!PhotonNetwork.IsConnected)
            {
                Debug.LogError("Не подключены к Photon!");
                return;
            }

            PhotonNetwork.JoinRandomRoom();
        }

        /// <summary>
        /// Присоединяется к комнате по имени
        /// </summary>
        public void JoinRoom(string roomName)
        {
            if (!PhotonNetwork.IsConnected)
            {
                Debug.LogError("Не подключены к Photon!");
                return;
            }

            PhotonNetwork.JoinRoom(roomName);
        }

        /// <summary>
        /// Покидает текущую комнату
        /// </summary>
        public void LeaveRoom()
        {
            PhotonNetwork.LeaveRoom();
        }

        #region Photon Callbacks

        public override void OnConnectedToMaster()
        {
            Debug.Log("✓ Подключены к Photon Master Server");
            PhotonNetwork.JoinLobby(); // Автоматически заходим в лобби
        }

        public override void OnJoinedLobby()
        {
            Debug.Log("✓ Вошли в лобби");
        }

        public override void OnCreatedRoom()
        {
            Debug.Log($"✓ Комната создана: {PhotonNetwork.CurrentRoom.Name}");
        }

        public override void OnJoinedRoom()
        {
            Debug.Log($"✓ Вошли в комнату: {PhotonNetwork.CurrentRoom.Name}");
            Debug.Log($"Игроков в комнате: {PhotonNetwork.CurrentRoom.PlayerCount}/{PhotonNetwork.CurrentRoom.MaxPlayers}");
        }

        public override void OnPlayerEnteredRoom(Photon.Realtime.Player newPlayer)
        {
            Debug.Log($"➤ Игрок присоединился: {newPlayer.NickName} (всего: {PhotonNetwork.CurrentRoom.PlayerCount})");
        }

        public override void OnPlayerLeftRoom(Photon.Realtime.Player otherPlayer)
        {
            Debug.Log($"➤ Игрок вышел: {otherPlayer.NickName} (осталось: {PhotonNetwork.CurrentRoom.PlayerCount})");
        }

        public override void OnLeftRoom()
        {
            Debug.Log("Вышли из комнаты");
        }

        public override void OnJoinRandomFailed(short returnCode, string message)
        {
            Debug.Log("Не найдена случайная комната. Создаем новую...");
            CreateRoom(); // Если нет комнат - создаем свою
        }

        public override void OnJoinRoomFailed(short returnCode, string message)
        {
            Debug.LogError($"Не удалось войти в комнату: {message}");
        }

        public override void OnDisconnected(DisconnectCause cause)
        {
            Debug.LogWarning($"Отключены от Photon: {cause}");
        }

        #endregion

        // Полезные публичные свойства
        public bool IsConnected => PhotonNetwork.IsConnected;
        public bool IsInRoom => PhotonNetwork.InRoom;
        public int PlayersInRoom => PhotonNetwork.CurrentRoom?.PlayerCount ?? 0;
        public string RoomName => PhotonNetwork.CurrentRoom?.Name ?? "Нет комнаты";
    }
}
