using UnityEngine;
using Photon.Pun;

namespace DarkDungeon.Managers
{
    /// <summary>
    /// Главный менеджер игры. Управляет игровым процессом в комнате.
    /// </summary>
    public class GameManager : MonoBehaviourPunCallbacks
    {
        public static GameManager Instance { get; private set; }

        [Header("Настройки игры")]
        [SerializeField] private int winScore = 10; // Сколько убийств для победы
        [SerializeField] private float roundTime = 600f; // Время раунда (10 минут)

        [Header("Spawn Points")]
        [SerializeField] private Transform[] spawnPoints;

        // Состояние игры
        private float roundTimer;
        private bool gameStarted = false;

        private void Awake()
        {
            // Singleton
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
        }

        private void Start()
        {
            roundTimer = roundTime;
            gameStarted = true;

            Debug.Log("🎮 Игра началась!");

            // Разблокируем курсор на случай если он был заблокирован в лобби
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }

        private void Update()
        {
            if (!gameStarted)
                return;

            // Таймер раунда
            roundTimer -= Time.deltaTime;
            if (roundTimer <= 0)
            {
                EndRound();
            }
        }

        /// <summary>
        /// Получить случайную точку спавна
        /// </summary>
        public Vector3 GetRandomSpawnPoint()
        {
            if (spawnPoints == null || spawnPoints.Length == 0)
            {
                // Если точек нет - возвращаем случайную позицию
                return new Vector3(
                    Random.Range(-10f, 10f),
                    2f,
                    Random.Range(-10f, 10f)
                );
            }

            int randomIndex = Random.Range(0, spawnPoints.Length);
            return spawnPoints[randomIndex].position;
        }

        /// <summary>
        /// Обработка убийства игрока
        /// </summary>
        public void OnPlayerKilled(string killerName, string victimName)
        {
            Debug.Log($"💀 {victimName} убит игроком {killerName}");

            // TODO: Добавить систему очков
            // TODO: Проверка условий победы
        }

        /// <summary>
        /// Завершение раунда
        /// </summary>
        private void EndRound()
        {
            gameStarted = false;
            Debug.Log("⏰ Раунд завершен!");

            // TODO: Показать экран результатов
            // TODO: Вернуться в лобби
        }

        /// <summary>
        /// Покинуть игру и вернуться в лобби
        /// </summary>
        public void LeaveGame()
        {
            PhotonNetwork.LeaveRoom();
            PhotonNetwork.LoadLevel("LobbyScene"); // Вернуться в лобби
        }

        // Визуализация точек спавна
        private void OnDrawGizmos()
        {
            if (spawnPoints == null || spawnPoints.Length == 0)
                return;

            Gizmos.color = Color.cyan;
            foreach (var point in spawnPoints)
            {
                if (point != null)
                {
                    Gizmos.DrawWireSphere(point.position, 1f);
                    Gizmos.DrawLine(point.position, point.position + Vector3.up * 3f);
                }
            }
        }

        public override void OnLeftRoom()
        {
            // Очищаем
            gameStarted = false;
        }

        // Публичные свойства
        public float RoundTimeRemaining => roundTimer;
        public bool IsGameStarted => gameStarted;
    }
}
