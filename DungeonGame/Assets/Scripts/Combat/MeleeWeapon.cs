using UnityEngine;
using Photon.Pun;
using System.Collections;

namespace DarkDungeon.Combat
{
    /// <summary>
    /// Оружие ближнего боя (меч, топор и т.д.)
    /// Поддерживает мультиплеер - атаки синхронизируются по сети.
    /// </summary>
    public class MeleeWeapon : MonoBehaviourPun
    {
        [Header("Параметры урона")]
        [SerializeField] private float damage = 25f;
        [SerializeField] private float attackRange = 2f;
        [SerializeField] private float attackAngle = 45f; // Угол атаки в градусах

        [Header("Таймингв атаки")]
        [SerializeField] private float attackCooldown = 0.8f;
        [SerializeField] private float attackDuration = 0.3f; // Время анимации удара

        [Header("Визуализация")]
        [SerializeField] private Transform attackPoint; // Точка откуда идет атака
        [SerializeField] private LayerMask hitLayers; // Что можно атаковать

        [Header("Эффекты")]
        [SerializeField] private GameObject hitEffectPrefab;
        [SerializeField] private AudioClip swingSound;
        [SerializeField] private AudioClip hitSound;

        // Состояние
        private float lastAttackTime;
        private bool isAttacking = false;
        private PhotonView ownerPhotonView;
        private AudioSource audioSource;

        // Публичные свойства
        public bool CanAttack => Time.time >= lastAttackTime + attackCooldown && !isAttacking;
        public float Damage => damage;

        private void Awake()
        {
            // Получаем PhotonView владельца (игрока)
            ownerPhotonView = GetComponentInParent<PhotonView>();

            // AudioSource для звуков
            audioSource = GetComponent<AudioSource>();
            if (audioSource == null)
                audioSource = gameObject.AddComponent<AudioSource>();

            // Если attackPoint не назначен, используем позицию оружия
            if (attackPoint == null)
                attackPoint = transform;

            // По умолчанию бьем все (если hitLayers не настроен в Inspector)
            if (hitLayers == 0)
            {
                hitLayers = ~0; // Все слои
                Debug.Log("⚠️ Hit Layers не настроены, используем все слои");
            }
        }

        /// <summary>
        /// Выполнить атаку (вызывается из PlayerCombat)
        /// </summary>
        public void Attack()
        {
            if (!CanAttack)
                return;

            if (ownerPhotonView != null && !ownerPhotonView.IsMine)
                return; // Только локальный игрок атакует

            Debug.Log("🗡️ Атака!");

            lastAttackTime = Time.time;
            isAttacking = true;

            // Запускаем корутину атаки
            StartCoroutine(AttackRoutine());

            // Синхронизируем атаку по сети
            if (ownerPhotonView != null)
            {
                ownerPhotonView.RPC(nameof(RPC_PlayAttackAnimation), RpcTarget.Others);
            }
        }

        /// <summary>
        /// Корутина выполнения атаки
        /// </summary>
        private IEnumerator AttackRoutine()
        {
            // Звук взмаха
            PlaySound(swingSound);

            // Небольшая задержка перед нанесением урона (реалистичность)
            yield return new WaitForSeconds(attackDuration * 0.5f);

            // Наносим урон
            PerformHit();

            // Ждем окончания анимации
            yield return new WaitForSeconds(attackDuration * 0.5f);

            isAttacking = false;
        }

        /// <summary>
        /// Проверка попадания и нанесение урона
        /// </summary>
        private void PerformHit()
        {
            Vector3 attackOrigin = attackPoint.position;
            Vector3 attackDirection = attackPoint.forward;

            // Находим всех потенциальных врагов в радиусе
            Collider[] hitColliders = Physics.OverlapSphere(attackOrigin, attackRange, hitLayers);

            Debug.Log($"Найдено коллайдеров в радиусе атаки: {hitColliders.Length}");

            foreach (Collider hit in hitColliders)
            {
                // Не атакуем себя
                if (hit.transform.root == transform.root)
                {
                    Debug.Log($"Пропускаем себя: {hit.name}");
                    continue;
                }

                // Проверяем угол атаки (атакуем только то, что перед нами)
                Vector3 directionToTarget = (hit.transform.position - attackOrigin).normalized;
                float angle = Vector3.Angle(attackDirection, directionToTarget);

                Debug.Log($"Цель: {hit.name}, угол: {angle}°, макс угол: {attackAngle}°");

                if (angle <= attackAngle)
                {
                    // Попадание!
                    DamageTarget(hit);
                }
            }
        }

        /// <summary>
        /// Нанести урон цели
        /// </summary>
        private void DamageTarget(Collider target)
        {
            // Пытаемся найти PlayerHealth
            var health = target.GetComponentInParent<Player.PlayerHealth>();
            if (health != null)
            {
                string attackerName = ownerPhotonView?.Owner?.NickName ?? "Unknown";
                health.TakeDamage(damage, attackerName);

                // Звук попадания
                PlaySound(hitSound);

                // Эффект попадания
                if (hitEffectPrefab != null)
                {
                    Vector3 hitPoint = target.ClosestPoint(attackPoint.position);
                    Instantiate(hitEffectPrefab, hitPoint, Quaternion.identity);
                }

                var targetPV = health.GetComponent<PhotonView>();
                string targetName = (targetPV != null && targetPV.Owner != null) ? targetPV.Owner.NickName : "Unknown";
                Debug.Log($"⚔️ Попадание! Нанесен урон {damage} игроку: {targetName}");
            }
            else
            {
                Debug.Log($"PlayerHealth не найден на цели: {target.name}");
            }

            // TODO: Можно добавить поддержку врагов (AI)
        }

        /// <summary>
        /// RPC для проигрывания анимации атаки у других игроков
        /// </summary>
        [PunRPC]
        private void RPC_PlayAttackAnimation()
        {
            // Проигрываем анимацию у удаленных игроков
            // TODO: Добавить Animator когда будут модели
            PlaySound(swingSound);
        }

        /// <summary>
        /// Воспроизвести звук
        /// </summary>
        private void PlaySound(AudioClip clip)
        {
            if (audioSource != null && clip != null)
            {
                audioSource.PlayOneShot(clip);
            }
        }

        // Визуализация зоны атаки в редакторе
        private void OnDrawGizmosSelected()
        {
            if (attackPoint == null)
                attackPoint = transform;

            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(attackPoint.position, attackRange);

            // Рисуем конус атаки
            Vector3 forward = attackPoint.forward * attackRange;
            Vector3 right = Quaternion.Euler(0, attackAngle, 0) * forward;
            Vector3 left = Quaternion.Euler(0, -attackAngle, 0) * forward;

            Gizmos.color = Color.yellow;
            Gizmos.DrawRay(attackPoint.position, forward);
            Gizmos.DrawRay(attackPoint.position, right);
            Gizmos.DrawRay(attackPoint.position, left);
        }
    }
}
