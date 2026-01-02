using UnityEngine;
using Photon.Pun;
using System;

namespace DarkDungeon.Player
{
    /// <summary>
    /// Система здоровья игрока с сетевой синхронизацией.
    /// Управляет HP, смертью и респавном.
    /// </summary>
    public class PlayerHealth : MonoBehaviourPun, IPunObservable
    {
        [Header("Настройки здоровья")]
        [SerializeField] private float maxHealth = 100f;
        [SerializeField] private float currentHealth;

        [Header("Регенерация")]
        [SerializeField] private bool enableHealthRegen = false;
        [SerializeField] private float healthRegenRate = 5f; // HP в секунду
        [SerializeField] private float healthRegenDelay = 5f; // задержка после урона

        [Header("Респавн")]
        [SerializeField] private float respawnDelay = 3f;

        // События
        public event Action<float, float> OnHealthChanged; // current, max
        public event Action<string> OnDeath; // имя убийцы
        public event Action OnRespawn;

        // Состояние
        private bool isDead = false;
        private float lastDamageTime;

        // Публичные свойства
        public float Health => currentHealth;
        public float MaxHealth => maxHealth;
        public bool IsDead => isDead;
        public float HealthPercent => currentHealth / maxHealth;

        private void Awake()
        {
            currentHealth = maxHealth;
        }

        private void Update()
        {
            // Проверка что PhotonView инициализирован
            if (photonView == null)
                return;

            // Регенерация только для локального игрока
            if (!photonView.IsMine || isDead || !enableHealthRegen)
                return;

            // Регенерация если прошло достаточно времени после урона
            if (Time.time - lastDamageTime >= healthRegenDelay && currentHealth < maxHealth)
            {
                float regenAmount = healthRegenRate * Time.deltaTime;
                Heal(regenAmount);
            }
        }

        /// <summary>
        /// Нанести урон (вызывается на всех клиентах через RPC)
        /// </summary>
        public void TakeDamage(float damage, string attackerName = "Unknown")
        {
            if (isDead || photonView == null)
                return;

            // Отправляем RPC всем
            photonView.RPC(nameof(RPC_TakeDamage), RpcTarget.All, damage, attackerName);
        }

        [PunRPC]
        private void RPC_TakeDamage(float damage, string attackerName)
        {
            currentHealth -= damage;
            currentHealth = Mathf.Max(0, currentHealth);
            lastDamageTime = Time.time;

            string playerName = (photonView != null && photonView.Owner != null) ? photonView.Owner.NickName : "Unknown";
            Debug.Log($"{playerName} получил {damage} урона от {attackerName}. HP: {currentHealth}/{maxHealth}");

            // Событие изменения здоровья
            OnHealthChanged?.Invoke(currentHealth, maxHealth);

            // Проверка смерти
            if (currentHealth <= 0 && !isDead)
            {
                Die(attackerName);
            }
        }

        /// <summary>
        /// Лечение
        /// </summary>
        public void Heal(float amount)
        {
            if (isDead)
                return;

            currentHealth += amount;
            currentHealth = Mathf.Min(maxHealth, currentHealth);

            OnHealthChanged?.Invoke(currentHealth, maxHealth);
        }

        /// <summary>
        /// Смерть игрока
        /// </summary>
        private void Die(string killerName)
        {
            if (isDead || photonView == null)
                return;

            isDead = true;

            string playerName = (photonView.Owner != null) ? photonView.Owner.NickName : "Unknown";
            Debug.Log($"💀 {playerName} убит игроком {killerName}");

            // Событие смерти
            OnDeath?.Invoke(killerName);

            // Отключаем управление для локального игрока
            if (photonView.IsMine)
            {
                var controller = GetComponent<FirstPersonController>();
                if (controller != null)
                    controller.enabled = false;

                // Запускаем респавн
                Invoke(nameof(Respawn), respawnDelay);
            }

            // Можно добавить визуальные эффекты смерти
            HandleDeathVisuals();
        }

        /// <summary>
        /// Респавн игрока
        /// </summary>
        private void Respawn()
        {
            if (photonView == null || !photonView.IsMine)
                return;

            string playerName = (photonView.Owner != null) ? photonView.Owner.NickName : "Unknown";
            Debug.Log($"♻️ {playerName} респавнится");

            // Восстанавливаем здоровье
            currentHealth = maxHealth;
            isDead = false;

            // Включаем управление
            var controller = GetComponent<FirstPersonController>();
            if (controller != null)
                controller.enabled = true;

            // Телепортируем в случайную точку
            TeleportToSpawn();

            // Событие респавна
            OnRespawn?.Invoke();
            OnHealthChanged?.Invoke(currentHealth, maxHealth);
        }

        /// <summary>
        /// Телепорт в точку спавна
        /// </summary>
        private void TeleportToSpawn()
        {
            // Простая телепортация в случайное место
            Vector3 randomPos = new Vector3(
                UnityEngine.Random.Range(-10f, 10f),
                2f,
                UnityEngine.Random.Range(-10f, 10f)
            );

            var controller = GetComponent<CharacterController>();
            if (controller != null)
            {
                controller.enabled = false;
                transform.position = randomPos;
                controller.enabled = true;
            }
            else
            {
                transform.position = randomPos;
            }
        }

        /// <summary>
        /// Визуальные эффекты смерти (Ragdoll, анимация и т.д.)
        /// </summary>
        private void HandleDeathVisuals()
        {
            // TODO: Добавить эффекты смерти
            // - Ragdoll
            // - Партиклы
            // - Звук
            // - Камера смерти

            // Пока просто скрываем модель
            var renderers = GetComponentsInChildren<Renderer>();
            foreach (var renderer in renderers)
            {
                renderer.enabled = false;
            }

            // Включим обратно при респавне
            if (photonView.IsMine)
            {
                Invoke(nameof(EnableRenderers), respawnDelay);
            }
        }

        private void EnableRenderers()
        {
            var renderers = GetComponentsInChildren<Renderer>();
            foreach (var renderer in renderers)
            {
                renderer.enabled = true;
            }
        }

        /// <summary>
        /// Синхронизация здоровья по сети (Photon)
        /// </summary>
        public void OnPhotonSerializeView(PhotonStream stream, PhotonMessageInfo info)
        {
            if (stream.IsWriting)
            {
                // Отправляем наше состояние другим
                stream.SendNext(currentHealth);
                stream.SendNext(isDead);
            }
            else
            {
                // Получаем состояние от других
                currentHealth = (float)stream.ReceiveNext();
                isDead = (bool)stream.ReceiveNext();

                OnHealthChanged?.Invoke(currentHealth, maxHealth);
            }
        }

        // Публичные методы для других систем
        public void SetMaxHealth(float newMaxHealth)
        {
            maxHealth = newMaxHealth;
            currentHealth = Mathf.Min(currentHealth, maxHealth);
            OnHealthChanged?.Invoke(currentHealth, maxHealth);
        }

        public void FullHeal()
        {
            Heal(maxHealth);
        }
    }
}
