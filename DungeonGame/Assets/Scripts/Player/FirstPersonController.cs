using UnityEngine;
using Photon.Pun;

namespace DarkDungeon.Player
{
    /// <summary>
    /// First-Person контроллер игрока с поддержкой мультиплеера.
    /// Управление: WASD - движение, Space - прыжок, Shift - бег, мышь - камера.
    /// </summary>
    [RequireComponent(typeof(CharacterController))]
    [RequireComponent(typeof(PhotonView))]
    public class FirstPersonController : MonoBehaviourPun
    {
        [Header("Движение")]
        [SerializeField] private float walkSpeed = 5f;
        [SerializeField] private float sprintSpeed = 8f;
        [SerializeField] private float crouchSpeed = 2.5f;
        [SerializeField] private float jumpHeight = 2f;
        [SerializeField] private float gravity = -19.62f;

        [Header("Камера")]
        [SerializeField] private Transform cameraTransform;
        [SerializeField] private float mouseSensitivity = 2f;
        [SerializeField] private float maxLookAngle = 80f;

        [Header("Выносливость")]
        [SerializeField] private float maxStamina = 100f;
        [SerializeField] private float sprintStaminaDrain = 20f; // в секунду
        [SerializeField] private float staminaRegenRate = 15f; // в секунду
        [SerializeField] private float staminaRegenDelay = 1f; // задержка перед реген

        // Компоненты
        private CharacterController characterController;
        private PhotonView photonView;

        // Состояние
        private Vector3 velocity;
        private float currentStamina;
        private float staminaRegenTimer;
        private bool isGrounded;
        private float cameraPitch = 0f;
        private bool isSprinting = false;

        // Публичные свойства
        public float Stamina => currentStamina;
        public float MaxStamina => maxStamina;
        public bool IsSprinting => isSprinting;

        private void Awake()
        {
            characterController = GetComponent<CharacterController>();
            photonView = GetComponent<PhotonView>();
            currentStamina = maxStamina;
        }

        private void Start()
        {
            // Настраиваем только для локального игрока
            if (photonView.IsMine)
            {
                SetupLocalPlayer();
            }
            else
            {
                SetupRemotePlayer();
            }
        }

        /// <summary>
        /// Настройка локального игрока (тот, кем мы управляем)
        /// </summary>
        private void SetupLocalPlayer()
        {
            // Находим камеру если не назначена
            if (cameraTransform == null)
            {
                cameraTransform = GetComponentInChildren<Camera>()?.transform;
            }

            if (cameraTransform != null)
            {
                cameraTransform.gameObject.SetActive(true);
            }

            // Блокируем курсор
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;

            Debug.Log("✓ Локальный игрок настроен");
        }

        /// <summary>
        /// Настройка удаленного игрока (другие игроки)
        /// </summary>
        private void SetupRemotePlayer()
        {
            // Отключаем камеру у других игроков
            if (cameraTransform != null)
            {
                cameraTransform.gameObject.SetActive(false);
            }

            // Отключаем этот скрипт для других игроков
            this.enabled = false;

            Debug.Log("✓ Удаленный игрок настроен");
        }

        private void Update()
        {
            // Только локальный игрок управляется
            if (!photonView.IsMine)
                return;

            // Проверка земли
            isGrounded = characterController.isGrounded;
            if (isGrounded && velocity.y < 0)
            {
                velocity.y = -2f; // Небольшое значение чтобы оставаться на земле
            }

            HandleMovement();
            HandleCamera();
            HandleStamina();

            // ESC для разблокировки курсора (для тестирования)
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                Cursor.lockState = CursorLockMode.None;
                Cursor.visible = true;
            }
        }

        /// <summary>
        /// Обработка движения игрока
        /// </summary>
        private void HandleMovement()
        {
            // Ввод
            float horizontal = Input.GetAxis("Horizontal");
            float vertical = Input.GetAxis("Vertical");

            // Определяем скорость
            bool wantsToSprint = Input.GetKey(KeyCode.LeftShift) && vertical > 0; // Бег только вперед
            float currentSpeed = walkSpeed;

            // Спринт (только если есть выносливость)
            if (wantsToSprint && currentStamina > 0)
            {
                currentSpeed = sprintSpeed;
                isSprinting = true;
            }
            else
            {
                isSprinting = false;
            }

            // Движение относительно направления взгляда
            Vector3 move = transform.right * horizontal + transform.forward * vertical;
            characterController.Move(move * currentSpeed * Time.deltaTime);

            // Прыжок
            if (Input.GetButtonDown("Jump") && isGrounded)
            {
                velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
            }

            // Гравитация
            velocity.y += gravity * Time.deltaTime;
            characterController.Move(velocity * Time.deltaTime);
        }

        /// <summary>
        /// Обработка камеры (мышь)
        /// </summary>
        private void HandleCamera()
        {
            if (cameraTransform == null)
                return;

            // Ввод мыши
            float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
            float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;

            // Поворот по Y (вращение тела)
            transform.Rotate(Vector3.up * mouseX);

            // Поворот камеры по X (вверх-вниз)
            cameraPitch -= mouseY;
            cameraPitch = Mathf.Clamp(cameraPitch, -maxLookAngle, maxLookAngle);
            cameraTransform.localRotation = Quaternion.Euler(cameraPitch, 0f, 0f);
        }

        /// <summary>
        /// Система выносливости
        /// </summary>
        private void HandleStamina()
        {
            if (isSprinting)
            {
                // Тратим выносливость
                currentStamina -= sprintStaminaDrain * Time.deltaTime;
                currentStamina = Mathf.Max(0, currentStamina);
                staminaRegenTimer = 0f; // Сбрасываем таймер регена
            }
            else
            {
                // Регенерация выносливости (с задержкой)
                staminaRegenTimer += Time.deltaTime;
                if (staminaRegenTimer >= staminaRegenDelay)
                {
                    currentStamina += staminaRegenRate * Time.deltaTime;
                    currentStamina = Mathf.Min(maxStamina, currentStamina);
                }
            }
        }

        // Публичные методы для других систем
        public void ModifyStamina(float amount)
        {
            currentStamina += amount;
            currentStamina = Mathf.Clamp(currentStamina, 0, maxStamina);
        }

        private void OnDrawGizmosSelected()
        {
            // Визуализация направления взгляда
            Gizmos.color = Color.blue;
            Gizmos.DrawRay(transform.position + Vector3.up, transform.forward * 2f);
        }
    }
}
