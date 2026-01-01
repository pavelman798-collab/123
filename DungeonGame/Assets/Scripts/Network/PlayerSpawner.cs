using UnityEngine;
using Photon.Pun;

namespace DarkDungeon.Network
{
    /// <summary>
    /// Спавнит игроков в комнате. Создает префаб игрока через Photon.
    /// </summary>
    public class PlayerSpawner : MonoBehaviourPunCallbacks
    {
        [Header("Настройки спавна")]
        [SerializeField] private string playerPrefabName = "Player"; // Имя префаба в Resources/
        [SerializeField] private Transform[] spawnPoints; // Точки спавна
        [SerializeField] private bool spawnOnStart = true;

        private void Start()
        {
            if (spawnOnStart && PhotonNetwork.IsConnectedAndReady && PhotonNetwork.InRoom)
            {
                SpawnPlayer();
            }
        }

        public override void OnJoinedRoom()
        {
            base.OnJoinedRoom();

            if (!spawnOnStart)
                return;

            // Небольшая задержка чтобы комната инициализировалась
            Invoke(nameof(SpawnPlayer), 0.5f);
        }

        /// <summary>
        /// Создает игрока в сети
        /// </summary>
        public void SpawnPlayer()
        {
            if (!PhotonNetwork.IsConnectedAndReady || !PhotonNetwork.InRoom)
            {
                Debug.LogError("Не можем заспавнить игрока - не в комнате!");
                return;
            }

            Vector3 spawnPosition = GetSpawnPosition();
            Quaternion spawnRotation = Quaternion.identity;

            // Создаем игрока через Photon
            GameObject player = PhotonNetwork.Instantiate(
                playerPrefabName,
                spawnPosition,
                spawnRotation
            );

            Debug.Log($"✓ Игрок заспавнен: {player.name} на позиции {spawnPosition}");
        }

        /// <summary>
        /// Получает позицию спавна (случайную из доступных точек)
        /// </summary>
        private Vector3 GetSpawnPosition()
        {
            // Если есть точки спавна - используем случайную
            if (spawnPoints != null && spawnPoints.Length > 0)
            {
                int randomIndex = Random.Range(0, spawnPoints.Length);
                return spawnPoints[randomIndex].position;
            }

            // Иначе спавним в случайном месте вокруг центра
            Vector3 randomOffset = new Vector3(
                Random.Range(-5f, 5f),
                1f, // Высота над полом
                Random.Range(-5f, 5f)
            );

            return randomOffset;
        }

        // Вспомогательный метод для визуализации точек спавна в редакторе
        private void OnDrawGizmos()
        {
            if (spawnPoints == null || spawnPoints.Length == 0)
                return;

            Gizmos.color = Color.green;
            foreach (var spawnPoint in spawnPoints)
            {
                if (spawnPoint != null)
                {
                    Gizmos.DrawWireSphere(spawnPoint.position, 0.5f);
                    Gizmos.DrawLine(spawnPoint.position, spawnPoint.position + Vector3.up * 2f);
                }
            }
        }
    }
}
