using UnityEngine;
using Photon.Pun;

namespace DarkDungeon.Player
{
    /// <summary>
    /// Управляет боевой системой игрока.
    /// Обрабатывает ввод атаки и управляет текущим оружием.
    /// </summary>
    public class PlayerCombat : MonoBehaviourPun
    {
        [Header("Оружие")]
        [SerializeField] private Combat.MeleeWeapon currentWeapon;
        [SerializeField] private Transform weaponHolder; // Где держим оружие (рука)

        [Header("Управление")]
        [SerializeField] private KeyCode attackKey = KeyCode.Mouse0; // ЛКМ
        [SerializeField] private KeyCode blockKey = KeyCode.Mouse1; // ПКМ (для будущего)

        // Состояние
        private bool isBlocking = false;

        private void Update()
        {
            // Только локальный игрок может атаковать
            if (!photonView.IsMine)
                return;

            HandleCombatInput();
        }

        /// <summary>
        /// Обработка ввода боя
        /// </summary>
        private void HandleCombatInput()
        {
            // Атака
            if (Input.GetKeyDown(attackKey) || Input.GetMouseButtonDown(0))
            {
                TryAttack();
            }

            // Блок (для будущего функционала)
            if (Input.GetKey(blockKey) || Input.GetMouseButton(1))
            {
                isBlocking = true;
            }
            else
            {
                isBlocking = false;
            }
        }

        /// <summary>
        /// Попытка атаковать
        /// </summary>
        private void TryAttack()
        {
            if (currentWeapon == null)
            {
                Debug.LogWarning("Нет оружия!");
                return;
            }

            if (isBlocking)
            {
                Debug.Log("Нельзя атаковать во время блока");
                return;
            }

            // Пытаемся атаковать
            currentWeapon.Attack();
        }

        /// <summary>
        /// Экипировать оружие
        /// </summary>
        public void EquipWeapon(Combat.MeleeWeapon weapon)
        {
            // Удаляем старое оружие
            if (currentWeapon != null)
            {
                Destroy(currentWeapon.gameObject);
            }

            currentWeapon = weapon;

            // Помещаем оружие в руку
            if (weaponHolder != null && weapon != null)
            {
                weapon.transform.SetParent(weaponHolder);
                weapon.transform.localPosition = Vector3.zero;
                weapon.transform.localRotation = Quaternion.identity;
            }

            Debug.Log($"Экипировано оружие: {weapon.name}");
        }

        /// <summary>
        /// Создать и экипировать оружие по префабу
        /// </summary>
        public void EquipWeaponFromPrefab(GameObject weaponPrefab)
        {
            if (weaponPrefab == null)
            {
                Debug.LogError("Префаб оружия пустой!");
                return;
            }

            // Создаем оружие
            GameObject weaponObj = Instantiate(weaponPrefab);
            Combat.MeleeWeapon weapon = weaponObj.GetComponent<Combat.MeleeWeapon>();

            if (weapon != null)
            {
                EquipWeapon(weapon);
            }
            else
            {
                Debug.LogError("На префабе нет компонента MeleeWeapon!");
                Destroy(weaponObj);
            }
        }

        // Публичные свойства
        public bool IsBlocking => isBlocking;
        public Combat.MeleeWeapon CurrentWeapon => currentWeapon;

        // Визуализация в редакторе
        private void OnDrawGizmosSelected()
        {
            if (weaponHolder != null)
            {
                Gizmos.color = Color.cyan;
                Gizmos.DrawWireSphere(weaponHolder.position, 0.1f);
            }
        }
    }
}
