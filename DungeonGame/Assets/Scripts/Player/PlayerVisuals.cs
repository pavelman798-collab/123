using UnityEngine;
using Photon.Pun;

namespace DarkDungeon.Player
{
    /// <summary>
    /// Управляет визуальным отображением игрока.
    /// Скрывает модель для локального игрока (первое лицо), показывает для других.
    /// </summary>
    public class PlayerVisuals : MonoBehaviourPun
    {
        [Header("Визуальная модель")]
        [SerializeField] private GameObject visualModel;

        private void Start()
        {
            // Если это наш локальный игрок - скрываем модель
            if (photonView.IsMine)
            {
                if (visualModel != null)
                {
                    // Отключаем только рендерер, коллайдер оставляем
                    var renderers = visualModel.GetComponentsInChildren<Renderer>();
                    foreach (var renderer in renderers)
                    {
                        renderer.enabled = false;
                    }

                    Debug.Log("Визуальная модель скрыта для локального игрока");
                }
            }
            else
            {
                Debug.Log("Визуальная модель видна для удаленного игрока");
            }
        }
    }
}
