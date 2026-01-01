using UnityEngine;
using UnityEngine.UI;
using TMPro;
using Photon.Pun;
using Photon.Realtime;

namespace DarkDungeon.UI
{
    /// <summary>
    /// UI лобби - подключение к серверу, создание/поиск комнат.
    /// </summary>
    public class LobbyUI : MonoBehaviourPunCallbacks
    {
        [Header("Панели")]
        [SerializeField] private GameObject connectingPanel;
        [SerializeField] private GameObject lobbyPanel;
        [SerializeField] private GameObject roomPanel;

        [Header("Lobby Panel Elements")]
        [SerializeField] private Button createRoomButton;
        [SerializeField] private Button joinRandomRoomButton;
        [SerializeField] private TMP_InputField roomNameInput;
        [SerializeField] private TMP_InputField playerNameInput;
        [SerializeField] private TextMeshProUGUI statusText;

        [Header("Room Panel Elements")]
        [SerializeField] private TextMeshProUGUI roomNameText;
        [SerializeField] private TextMeshProUGUI playerListText;
        [SerializeField] private Button startGameButton;
        [SerializeField] private Button leaveRoomButton;

        [Header("Настройки")]
        [SerializeField] private string gameSceneName = "GameScene";

        private void Start()
        {
            // Показываем панель подключения
            ShowPanel(connectingPanel);

            // Настраиваем кнопки
            if (createRoomButton != null)
                createRoomButton.onClick.AddListener(OnCreateRoomClicked);

            if (joinRandomRoomButton != null)
                joinRandomRoomButton.onClick.AddListener(OnJoinRandomRoomClicked);

            if (startGameButton != null)
                startGameButton.onClick.AddListener(OnStartGameClicked);

            if (leaveRoomButton != null)
                leaveRoomButton.onClick.AddListener(OnLeaveRoomClicked);

            // Загружаем сохраненное имя игрока
            if (playerNameInput != null)
            {
                string savedName = PlayerPrefs.GetString("PlayerName", "Player" + Random.Range(1000, 9999));
                playerNameInput.text = savedName;
                PhotonNetwork.NickName = savedName;
            }

            UpdateStatus("Подключение к серверу...");
        }

        #region Photon Callbacks

        public override void OnConnectedToMaster()
        {
            UpdateStatus("Подключено к серверу");
            ShowPanel(lobbyPanel);
        }

        public override void OnJoinedLobby()
        {
            UpdateStatus("В лобби. Готовы к игре!");
        }

        public override void OnJoinedRoom()
        {
            UpdateStatus($"В комнате: {PhotonNetwork.CurrentRoom.Name}");
            ShowPanel(roomPanel);
            UpdateRoomInfo();
        }

        public override void OnPlayerEnteredRoom(Photon.Realtime.Player newPlayer)
        {
            UpdateRoomInfo();
            UpdateStatus($"{newPlayer.NickName} присоединился к комнате");
        }

        public override void OnPlayerLeftRoom(Photon.Realtime.Player otherPlayer)
        {
            UpdateRoomInfo();
            UpdateStatus($"{otherPlayer.NickName} покинул комнату");
        }

        public override void OnLeftRoom()
        {
            ShowPanel(lobbyPanel);
            UpdateStatus("Вышли из комнаты");
        }

        public override void OnCreateRoomFailed(short returnCode, string message)
        {
            UpdateStatus($"Ошибка создания комнаты: {message}");
        }

        public override void OnJoinRoomFailed(short returnCode, string message)
        {
            UpdateStatus($"Ошибка входа в комнату: {message}");
        }

        public override void OnJoinRandomFailed(short returnCode, string message)
        {
            UpdateStatus("Комнаты не найдены. Создаем новую...");
            OnCreateRoomClicked();
        }

        #endregion

        #region Button Handlers

        private void OnCreateRoomClicked()
        {
            if (!PhotonNetwork.IsConnectedAndReady)
            {
                UpdateStatus("Не подключены к серверу!");
                return;
            }

            // Обновляем имя игрока
            UpdatePlayerName();

            // Получаем имя комнаты
            string roomName = roomNameInput != null && !string.IsNullOrEmpty(roomNameInput.text)
                ? roomNameInput.text
                : "Room_" + Random.Range(1000, 9999);

            UpdateStatus($"Создание комнаты: {roomName}...");

            // Создаем комнату
            RoomOptions roomOptions = new RoomOptions
            {
                MaxPlayers = 4,
                IsVisible = true,
                IsOpen = true
            };

            PhotonNetwork.CreateRoom(roomName, roomOptions);
        }

        private void OnJoinRandomRoomClicked()
        {
            if (!PhotonNetwork.IsConnectedAndReady)
            {
                UpdateStatus("Не подключены к серверу!");
                return;
            }

            UpdatePlayerName();
            UpdateStatus("Поиск комнаты...");
            PhotonNetwork.JoinRandomRoom();
        }

        private void OnStartGameClicked()
        {
            if (!PhotonNetwork.IsMasterClient)
            {
                UpdateStatus("Только хост может начать игру!");
                return;
            }

            UpdateStatus("Загрузка игры...");

            // Закрываем комнату для новых игроков
            PhotonNetwork.CurrentRoom.IsOpen = false;
            PhotonNetwork.CurrentRoom.IsVisible = false;

            // Загружаем игровую сцену для всех
            PhotonNetwork.LoadLevel(gameSceneName);
        }

        private void OnLeaveRoomClicked()
        {
            UpdateStatus("Выход из комнаты...");
            PhotonNetwork.LeaveRoom();
        }

        #endregion

        #region Helper Methods

        private void UpdatePlayerName()
        {
            if (playerNameInput != null && !string.IsNullOrEmpty(playerNameInput.text))
            {
                PhotonNetwork.NickName = playerNameInput.text;
                PlayerPrefs.SetString("PlayerName", playerNameInput.text);
            }
        }

        private void UpdateRoomInfo()
        {
            if (!PhotonNetwork.InRoom)
                return;

            // Имя комнаты
            if (roomNameText != null)
            {
                roomNameText.text = $"Комната: {PhotonNetwork.CurrentRoom.Name}";
            }

            // Список игроков
            if (playerListText != null)
            {
                string playerList = $"Игроки ({PhotonNetwork.CurrentRoom.PlayerCount}/{PhotonNetwork.CurrentRoom.MaxPlayers}):\n";
                foreach (var player in PhotonNetwork.PlayerList)
                {
                    string prefix = player.IsMasterClient ? "[HOST] " : "";
                    playerList += $"{prefix}{player.NickName}\n";
                }
                playerListText.text = playerList;
            }

            // Кнопка старта только для хоста
            if (startGameButton != null)
            {
                startGameButton.interactable = PhotonNetwork.IsMasterClient;
            }
        }

        private void UpdateStatus(string message)
        {
            if (statusText != null)
            {
                statusText.text = message;
            }

            Debug.Log($"[LobbyUI] {message}");
        }

        private void ShowPanel(GameObject panel)
        {
            // Скрываем все панели
            if (connectingPanel != null) connectingPanel.SetActive(false);
            if (lobbyPanel != null) lobbyPanel.SetActive(false);
            if (roomPanel != null) roomPanel.SetActive(false);

            // Показываем нужную
            if (panel != null) panel.SetActive(true);
        }

        #endregion
    }
}
