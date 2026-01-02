using UnityEngine;
using Photon.Pun;

namespace DarkDungeon.Network
{
    /// <summary>
    /// Автоматически создает или присоединяется к комнате при старте GameScene
    /// </summary>
    public class AutoJoinRoom : MonoBehaviourPunCallbacks
    {
        [SerializeField] private string roomName = "TestRoom";

        private void Start()
        {
            if (!PhotonNetwork.IsConnected)
            {
                Debug.Log("Ждем подключения к Photon...");
                return;
            }

            TryJoinOrCreateRoom();
        }

        public override void OnConnectedToMaster()
        {
            Debug.Log("AutoJoin: Подключились к Photon, входим в комнату...");
            TryJoinOrCreateRoom();
        }

        public override void OnJoinedLobby()
        {
            TryJoinOrCreateRoom();
        }

        private void TryJoinOrCreateRoom()
        {
            if (PhotonNetwork.InRoom)
            {
                Debug.Log("Уже в комнате!");
                return;
            }

            Debug.Log($"Пытаемся войти в комнату: {roomName}");
            PhotonNetwork.JoinOrCreateRoom(roomName,
                new Photon.Realtime.RoomOptions { MaxPlayers = 4 },
                Photon.Realtime.TypedLobby.Default);
        }

        public override void OnJoinedRoom()
        {
            Debug.Log($"✓ AutoJoin: Вошли в комнату {PhotonNetwork.CurrentRoom.Name}!");
        }
    }
}
