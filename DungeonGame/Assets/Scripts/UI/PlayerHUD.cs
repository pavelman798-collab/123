using UnityEngine;
using UnityEngine.UI;
using TMPro;

namespace DarkDungeon.UI
{
    /// <summary>
    /// HUD игрока - отображает здоровье, выносливость и другую информацию.
    /// </summary>
    public class PlayerHUD : MonoBehaviour
    {
        [Header("Ссылки на UI элементы")]
        [SerializeField] private Image healthBarFill;
        [SerializeField] private Image staminaBarFill;
        [SerializeField] private TextMeshProUGUI healthText;
        [SerializeField] private TextMeshProUGUI staminaText;
        [SerializeField] private TextMeshProUGUI killFeedText;
        [SerializeField] private GameObject deathScreen;
        [SerializeField] private TextMeshProUGUI respawnTimerText;

        [Header("Настройки")]
        [SerializeField] private Color healthColor = Color.green;
        [SerializeField] private Color healthLowColor = Color.red;
        [SerializeField] private float healthLowThreshold = 0.3f;
        [SerializeField] private Color staminaColor = Color.yellow;

        // Ссылки на компоненты игрока
        private Player.PlayerHealth playerHealth;
        private Player.FirstPersonController playerController;

        // Состояние
        private float respawnTimer;

        private void Start()
        {
            // Находим локального игрока
            FindLocalPlayer();

            // Скрываем экран смерти
            if (deathScreen != null)
                deathScreen.SetActive(false);

            // Применяем цвета
            if (healthBarFill != null)
                healthBarFill.color = healthColor;

            if (staminaBarFill != null)
                staminaBarFill.color = staminaColor;
        }

        /// <summary>
        /// Находит локального игрока и подписывается на события
        /// </summary>
        private void FindLocalPlayer()
        {
            // Ждем пока игрок заспавнится
            Invoke(nameof(FindPlayerComponents), 1f);
        }

        private void FindPlayerComponents()
        {
            // Ищем всех игроков
            var players = FindObjectsOfType<Player.PlayerHealth>();

            Debug.Log($"Найдено игроков: {players.Length}");

            foreach (var player in players)
            {
                var pv = player.GetComponent<Photon.Pun.PhotonView>();
                if (pv != null && pv.IsMine)
                {
                    playerHealth = player;
                    playerController = player.GetComponent<Player.FirstPersonController>();

                    // Подписываемся на события
                    playerHealth.OnHealthChanged += UpdateHealthBar;
                    playerHealth.OnDeath += ShowDeathScreen;
                    playerHealth.OnRespawn += HideDeathScreen;

                    Debug.Log("✓ HUD подключен к локальному игроку");

                    // Инициализируем полоски сразу
                    UpdateHealthBar(playerHealth.Health, playerHealth.MaxHealth);
                    if (playerController != null)
                    {
                        UpdateStaminaBar(playerController.Stamina, playerController.MaxStamina);
                    }

                    return;
                }
            }

            Debug.Log("Локальный игрок не найден, попытка через 1 сек...");

            // Если не нашли - попробуем еще раз через секунду
            Invoke(nameof(FindPlayerComponents), 1f);
        }

        private void Update()
        {
            // Обновляем выносливость каждый кадр
            if (playerController != null)
            {
                UpdateStaminaBar(playerController.Stamina, playerController.MaxStamina);
            }

            // Таймер респавна
            if (respawnTimer > 0)
            {
                respawnTimer -= Time.deltaTime;
                if (respawnTimerText != null)
                {
                    respawnTimerText.text = $"Респавн через: {Mathf.Ceil(respawnTimer)}с";
                }
            }
        }

        /// <summary>
        /// Обновление полоски здоровья
        /// </summary>
        private void UpdateHealthBar(float current, float max)
        {
            float healthPercent = current / max;

            // Обновляем заполнение
            if (healthBarFill != null)
            {
                healthBarFill.fillAmount = healthPercent;

                // Меняем цвет если здоровье низкое
                healthBarFill.color = healthPercent <= healthLowThreshold ? healthLowColor : healthColor;
            }

            // Обновляем текст
            if (healthText != null)
            {
                healthText.text = $"{Mathf.Ceil(current)}/{max}";
            }
        }

        /// <summary>
        /// Обновление полоски выносливости
        /// </summary>
        private void UpdateStaminaBar(float current, float max)
        {
            float staminaPercent = current / max;

            // Обновляем заполнение
            if (staminaBarFill != null)
            {
                staminaBarFill.fillAmount = staminaPercent;
            }

            // Обновляем текст
            if (staminaText != null)
            {
                staminaText.text = $"{Mathf.Ceil(current)}/{max}";
            }
        }

        /// <summary>
        /// Показать экран смерти
        /// </summary>
        private void ShowDeathScreen(string killerName)
        {
            if (deathScreen != null)
            {
                deathScreen.SetActive(true);
            }

            // Показываем кто убил
            AddKillFeed($"Вы убиты игроком: {killerName}");

            // Запускаем таймер респавна
            respawnTimer = 3f;
        }

        /// <summary>
        /// Скрыть экран смерти
        /// </summary>
        private void HideDeathScreen()
        {
            if (deathScreen != null)
            {
                deathScreen.SetActive(false);
            }

            respawnTimer = 0;
        }

        /// <summary>
        /// Добавить сообщение в килл-фид
        /// </summary>
        public void AddKillFeed(string message)
        {
            if (killFeedText != null)
            {
                killFeedText.text = message + "\n" + killFeedText.text;

                // Ограничиваем длину (последние 5 сообщений)
                string[] lines = killFeedText.text.Split('\n');
                if (lines.Length > 5)
                {
                    killFeedText.text = string.Join("\n", lines, 0, 5);
                }
            }
        }

        private void OnDestroy()
        {
            // Отписываемся от событий
            if (playerHealth != null)
            {
                playerHealth.OnHealthChanged -= UpdateHealthBar;
                playerHealth.OnDeath -= ShowDeathScreen;
                playerHealth.OnRespawn -= HideDeathScreen;
            }
        }
    }
}
