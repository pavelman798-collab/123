// ============================================
// API для работы с телефонными кампаниями
// ============================================

const API_BASE = '/api';

// ============================================
// Утилиты
// ============================================

function showNotification(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.role = 'alert';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container-fluid');
    container.insertBefore(toast, container.firstChild);

    setTimeout(() => toast.remove(), 5000);
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU');
}

function formatPhoneNumber(phone) {
    // Форматирует 79991234567 -> +7 (999) 123-45-67
    if (!phone) return '-';
    return phone.replace(/(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/, '+$1 ($2) $3-$4-$5');
}

// ============================================
// Навигация
// ============================================

function showSection(sectionName) {
    // Скрыть все секции
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });

    // Показать нужную секцию
    const section = document.getElementById(sectionName + 'Section');
    if (section) {
        section.style.display = 'block';
    }

    // Обновить активный пункт меню
    document.querySelectorAll('.list-group-item').forEach(item => {
        item.classList.remove('active');
    });

    // Загрузить данные для секции
    switch(sectionName) {
        case 'campaigns':
            loadCampaigns();
            break;
        case 'newCampaign':
            loadAudioFilesForCampaign();
            // Загружаем все шаблоны для обоих dropdown
            loadSMSTemplates(null, 'smsNoAnswerTemplate');
            loadSMSTemplates(null, 'smsSuccessTemplate');
            break;
        case 'tts':
            loadTTSFiles();
            break;
        case 'sims':
            loadSimCards();
            break;
        case 'stats':
            loadStatistics();
            break;
    }
}

// ============================================
// Загрузка данных
// ============================================

async function loadCampaigns() {
    try {
        const response = await fetch(`${API_BASE}/campaigns`);
        const data = await response.json();

        const container = document.getElementById('campaignsList');

        if (data.campaigns.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 4rem; color: #CCC;"></i>
                    <p class="mt-3 text-muted">Нет кампаний. Создайте первую!</p>
                    <button class="btn btn-danger" onclick="showSection('newCampaign')">
                        <i class="bi bi-plus-lg"></i> Создать кампанию
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = data.campaigns.map(campaign => `
            <div class="card campaign-card mb-3" onclick="showCampaignDetails(${campaign.id})">
                <div class="card-body position-relative">
                    <span class="badge bg-${getStatusColor(campaign.status)} campaign-status-badge">
                        ${getStatusText(campaign.status)}
                    </span>

                    <h5 class="card-title">${campaign.name}</h5>
                    <p class="card-text text-muted">${campaign.description || 'Без описания'}</p>

                    <div class="row mt-3">
                        <div class="col-md-3">
                            <small class="text-muted">Всего номеров</small>
                            <div class="fw-bold">${campaign.total_numbers}</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">Обработано</small>
                            <div class="fw-bold text-primary">${campaign.processed_numbers}</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">Успешных</small>
                            <div class="fw-bold text-success">${campaign.successful_calls}</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">Неудачных</small>
                            <div class="fw-bold text-danger">${campaign.failed_calls}</div>
                        </div>
                    </div>

                    ${campaign.total_numbers > 0 ? `
                        <div class="progress mt-3">
                            <div class="progress-bar bg-success" style="width: ${(campaign.processed_numbers / campaign.total_numbers * 100).toFixed(1)}%"></div>
                        </div>
                        <small class="text-muted">${(campaign.processed_numbers / campaign.total_numbers * 100).toFixed(1)}% завершено</small>
                    ` : ''}

                    <div class="campaign-actions mt-3">
                        ${campaign.status === 'draft' || campaign.status === 'paused' ? `
                            <button class="btn btn-sm btn-success" onclick="event.stopPropagation(); startCampaign(${campaign.id})">
                                <i class="bi bi-play-fill"></i> Старт
                            </button>
                        ` : ''}
                        ${campaign.status === 'running' ? `
                            <button class="btn btn-sm btn-warning" onclick="event.stopPropagation(); pauseCampaign(${campaign.id})">
                                <i class="bi bi-pause-fill"></i> Пауза
                            </button>
                        ` : ''}
                        <button class="btn btn-sm btn-info text-white" onclick="event.stopPropagation(); showCampaignDetails(${campaign.id})">
                            <i class="bi bi-bar-chart"></i> Статистика
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Ошибка загрузки кампаний:', error);
        showNotification('Ошибка загрузки кампаний', 'danger');
    }
}

async function loadSimCards() {
    try {
        const response = await fetch(`${API_BASE}/sims`);
        const data = await response.json();

        const container = document.getElementById('simCardsList');

        container.innerHTML = data.sims.map((sim, index) => `
            <div class="col-md-6 mb-3">
                <div class="card sim-card ${sim.status !== 'active' ? 'border-secondary' : ''}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h5 class="card-title">
                                    <i class="bi bi-sim-fill operator-${sim.operator.toLowerCase()}"></i>
                                    SIM ${sim.sim_number} - ${sim.operator}
                                </h5>
                                <p class="text-muted mb-1">
                                    <i class="bi bi-telephone"></i> ${formatPhoneNumber(sim.phone_number)}
                                </p>
                            </div>
                            <span class="badge bg-${sim.status === 'active' ? 'success' : 'secondary'}">
                                ${sim.status === 'active' ? 'Активна' : 'Неактивна'}
                            </span>
                        </div>

                        <div class="row mt-3">
                            <div class="col-6">
                                <small class="text-muted">Звонков сегодня</small>
                                <div class="progress mt-1">
                                    <div class="progress-bar ${sim.calls_today >= sim.daily_call_limit ? 'bg-danger' : 'bg-success'}"
                                         style="width: ${(sim.calls_today / sim.daily_call_limit * 100).toFixed(0)}%">
                                    </div>
                                </div>
                                <small>${sim.calls_today} / ${sim.daily_call_limit}</small>
                            </div>
                            <div class="col-6">
                                <small class="text-muted">Звонков за час</small>
                                <div class="progress mt-1">
                                    <div class="progress-bar ${sim.calls_this_hour >= sim.hourly_call_limit ? 'bg-danger' : 'bg-info'}"
                                         style="width: ${(sim.calls_this_hour / sim.hourly_call_limit * 100).toFixed(0)}%">
                                    </div>
                                </div>
                                <small>${sim.calls_this_hour} / ${sim.hourly_call_limit}</small>
                            </div>
                        </div>

                        ${sim.last_call_time ? `
                            <div class="mt-2">
                                <small class="text-muted">
                                    <i class="bi bi-clock"></i> Последний звонок: ${formatDate(sim.last_call_time)}
                                </small>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');

        // Обновить виджет в сайдбаре
        updateSimWidget(data.sims);

    } catch (error) {
        console.error('Ошибка загрузки SIM-карт:', error);
        showNotification('Ошибка загрузки SIM-карт', 'danger');
    }
}

function updateSimWidget(sims) {
    const widget = document.getElementById('simCardsWidget');

    widget.innerHTML = sims.map(sim => `
        <div class="sim-card-mini ${sim.status !== 'active' ? 'disabled' : ''}">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>SIM${sim.sim_number}</strong> ${sim.operator}
                </div>
                <small class="text-muted">${sim.calls_today}/${sim.daily_call_limit}</small>
            </div>
        </div>
    `).join('');
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/campaigns`);
        const data = await response.json();

        const totalCampaigns = data.campaigns.length;
        const activeCampaigns = data.campaigns.filter(c => c.status === 'running').length;
        const totalSuccess = data.campaigns.reduce((sum, c) => sum + (c.successful_calls || 0), 0);
        const totalFailed = data.campaigns.reduce((sum, c) => sum + (c.failed_calls || 0), 0);

        document.getElementById('totalCampaigns').textContent = totalCampaigns;
        document.getElementById('activeCampaigns').textContent = activeCampaigns;
        document.getElementById('totalSuccess').textContent = totalSuccess;
        document.getElementById('totalFailed').textContent = totalFailed;

    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
    }
}

async function showCampaignDetails(campaignId) {
    try {
        const response = await fetch(`${API_BASE}/campaigns/${campaignId}/stats`);
        const stats = await response.json();

        const modalTitle = document.getElementById('campaignModalTitle');
        const modalBody = document.getElementById('campaignModalBody');

        modalTitle.textContent = stats.name;

        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center">
                    <h6 class="text-muted">Всего номеров</h6>
                    <h3>${stats.total_numbers}</h3>
                </div>
                <div class="col-md-4 text-center">
                    <h6 class="text-muted">Обработано</h6>
                    <h3 class="text-primary">${stats.processed_numbers}</h3>
                </div>
                <div class="col-md-4 text-center">
                    <h6 class="text-muted">Успешных</h6>
                    <h3 class="text-success">${stats.successful_calls}</h3>
                </div>
            </div>

            <hr>

            <h6>Детальная статистика:</h6>
            <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between">
                    <span><i class="bi bi-hourglass-split text-warning"></i> В ожидании</span>
                    <strong>${stats.pending || 0}</strong>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                    <span><i class="bi bi-check-circle text-success"></i> Ответили</span>
                    <strong>${stats.answered || 0}</strong>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                    <span><i class="bi bi-x-circle text-danger"></i> Не ответили</span>
                    <strong>${stats.no_answer || 0}</strong>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                    <span><i class="bi bi-telephone-x text-warning"></i> Занято</span>
                    <strong>${stats.busy || 0}</strong>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                    <span><i class="bi bi-exclamation-triangle text-danger"></i> Ошибка</span>
                    <strong>${stats.failed || 0}</strong>
                </li>
            </ul>
        `;

        const modal = new bootstrap.Modal(document.getElementById('campaignModal'));
        modal.show();

    } catch (error) {
        console.error('Ошибка загрузки статистики кампании:', error);
        showNotification('Ошибка загрузки статистики', 'danger');
    }
}

// ============================================
// Действия с кампаниями
// ============================================

async function startCampaign(campaignId) {
    try {
        const response = await fetch(`${API_BASE}/campaigns/${campaignId}/start`, {
            method: 'POST'
        });

        if (response.ok) {
            showNotification('Кампания запущена!', 'success');
            loadCampaigns();
        } else {
            throw new Error('Ошибка запуска');
        }
    } catch (error) {
        showNotification('Ошибка запуска кампании', 'danger');
    }
}

async function pauseCampaign(campaignId) {
    try {
        const response = await fetch(`${API_BASE}/campaigns/${campaignId}/pause`, {
            method: 'POST'
        });

        if (response.ok) {
            showNotification('Кампания приостановлена', 'warning');
            loadCampaigns();
        } else {
            throw new Error('Ошибка паузы');
        }
    } catch (error) {
        showNotification('Ошибка остановки кампании', 'danger');
    }
}

// ============================================
// Создание кампании
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('newCampaignForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('campaignName').value;
        const description = document.getElementById('campaignDescription').value;
        const campaignType = document.getElementById('campaignType').value;
        const audioFile = document.getElementById('audioFile').value;
        const numbersFile = document.getElementById('numbersFile').files[0];

        // SMS fields
        const sendSmsOnNoAnswer = document.getElementById('sendSmsOnNoAnswer').checked;
        const sendSmsOnSuccess = document.getElementById('sendSmsOnSuccess').checked;
        const smsNoAnswerText = document.getElementById('smsNoAnswerText').value;
        const smsSuccessText = document.getElementById('smsSuccessText').value;

        try {
            // Создаем кампанию
            const createResponse = await fetch(`${API_BASE}/campaigns`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name,
                    description,
                    campaign_type: campaignType,
                    audio_file: audioFile || null,
                    sms_on_no_answer: smsNoAnswerText || null,
                    sms_on_success: smsSuccessText || null,
                    send_sms_on_no_answer: sendSmsOnNoAnswer,
                    send_sms_on_success: sendSmsOnSuccess
                })
            });

            if (!createResponse.ok) throw new Error('Ошибка создания кампании');

            const { campaign_id } = await createResponse.json();

            // Загружаем номера, если файл выбран
            if (numbersFile) {
                const formData = new FormData();
                formData.append('file', numbersFile);

                const uploadResponse = await fetch(`${API_BASE}/campaigns/${campaign_id}/numbers`, {
                    method: 'POST',
                    body: formData
                });

                if (!uploadResponse.ok) throw new Error('Ошибка загрузки номеров');
            }

            showNotification('Кампания создана успешно!', 'success');
            form.reset();
            showSection('campaigns');

        } catch (error) {
            console.error('Ошибка:', error);
            showNotification(error.message, 'danger');
        }
    });
});

// ============================================
// TTS - Генератор голоса
// ============================================

async function loadAudioFilesForCampaign() {
    /**
     * Загружает список аудио файлов для выбора при создании кампании
     */
    try {
        const response = await fetch(`${API_BASE}/tts/files`);
        const data = await response.json();

        const select = document.getElementById('audioFile');

        // Очищаем options кроме первого
        select.innerHTML = '<option value="">-- Без аудио --</option>';

        if (data.total > 0) {
            data.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file.filename;
                option.textContent = `${file.filename} (${(file.size / 1024).toFixed(1)} KB)`;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Ошибка загрузки аудио файлов:', error);
    }
}

async function loadTTSFiles() {
    try {
        const response = await fetch(`${API_BASE}/tts/files`);
        const data = await response.json();

        const container = document.getElementById('ttsFilesList');

        if (data.total === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-3">
                    <i class="bi bi-file-earmark-music" style="font-size: 2rem;"></i>
                    <p class="mt-2">Нет сгенерированных файлов</p>
                </div>
            `;
            return;
        }

        container.innerHTML = data.files.map(file => `
            <div class="tts-file-item border-bottom pb-2 mb-2">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <strong>${file.filename}</strong>
                        <br>
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${new Date(file.created).toLocaleString('ru-RU')}
                            <br>
                            <i class="bi bi-file-earmark"></i> ${(file.size / 1024).toFixed(1)} KB
                        </small>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-primary" onclick="playAudio('${file.filename}')">
                            <i class="bi bi-play"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Ошибка загрузки файлов:', error);
        const container = document.getElementById('ttsFilesList');
        container.innerHTML = `
            <div class="alert alert-warning">
                <i class="bi bi-exclamation-triangle"></i>
                TTS сервис недоступен
            </div>
        `;
    }
}

function playAudio(filename) {
    const audioPlayer = document.getElementById('audioPlayer');
    const audioSource = document.getElementById('audioSource');

    audioSource.src = `/api/tts/audio/${filename}`;
    audioPlayer.load();
    audioPlayer.play();

    // Прокручиваем к плееру и показываем результат
    document.getElementById('ttsResult').style.display = 'block';
    document.getElementById('generatedFilename').textContent = filename;
}

// Обработчик формы TTS
document.addEventListener('DOMContentLoaded', () => {
    const ttsForm = document.getElementById('ttsForm');
    const ttsTextarea = document.getElementById('ttsText');
    const textLength = document.getElementById('textLength');
    const generateBtn = document.getElementById('generateBtn');
    const ttsResult = document.getElementById('ttsResult');
    const ttsError = document.getElementById('ttsError');
    const ttsSpeed = document.getElementById('ttsSpeed');
    const speedValue = document.getElementById('speedValue');

    // Счетчик символов
    if (ttsTextarea) {
        ttsTextarea.addEventListener('input', () => {
            textLength.textContent = ttsTextarea.value.length;
        });
    }

    // Обновление значения скорости
    if (ttsSpeed) {
        ttsSpeed.addEventListener('input', () => {
            speedValue.textContent = ttsSpeed.value + 'x';
        });
    }

    // Отправка формы
    if (ttsForm) {
        ttsForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const text = ttsTextarea.value.trim();
            const filename = document.getElementById('ttsFilename').value.trim();
            const voice = document.getElementById('ttsVoice').value;
            const speed = parseFloat(ttsSpeed.value);

            if (!text) {
                ttsError.style.display = 'block';
                document.getElementById('errorText').textContent = 'Введите текст для генерации';
                return;
            }

            // Скрыть предыдущие сообщения
            ttsResult.style.display = 'none';
            ttsError.style.display = 'none';

            // Показываем загрузку
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Генерация...';

            try {
                // Формируем тело запроса
                const requestBody = {
                    text: text,
                    voice: voice,
                    speed: speed
                };
                if (filename) {
                    requestBody.filename = filename;
                }

                const response = await fetch(`${API_BASE}/tts/generate`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    // Успешно сгенерировано
                    document.getElementById('generatedFilename').textContent = data.filename;

                    // Загружаем аудио в плеер
                    const audioPlayer = document.getElementById('audioPlayer');
                    const audioSource = document.getElementById('audioSource');
                    audioSource.src = `/api/tts/audio/${data.filename}`;
                    audioPlayer.load();

                    ttsResult.style.display = 'block';

                    // Обновляем список файлов
                    loadTTSFiles();

                    showNotification('Голос успешно сгенерирован!', 'success');

                } else {
                    throw new Error(data.detail || 'Ошибка генерации');
                }

            } catch (error) {
                console.error('Ошибка TTS:', error);
                ttsError.style.display = 'block';
                document.getElementById('errorText').textContent = error.message;
                showNotification('Ошибка генерации голоса', 'danger');
            } finally {
                // Восстанавливаем кнопку
                generateBtn.disabled = false;
                generateBtn.innerHTML = '<i class="bi bi-play-circle"></i> Сгенерировать голос';
            }
        });
    }
});

// ============================================
// SMS - Управление шаблонами и кампаниями
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const campaignType = document.getElementById('campaignType');
    const audioFileSection = document.getElementById('audioFileSection');
    const smsSection = document.getElementById('smsSection');
    const smsNoAnswerSection = document.getElementById('smsNoAnswerSection');
    const smsSuccessSection = document.getElementById('smsSuccessSection');

    // Обработчик изменения типа кампании
    if (campaignType) {
        campaignType.addEventListener('change', () => {
            const type = campaignType.value;

            // Показываем/скрываем секции в зависимости от типа
            if (type === 'call') {
                // Только звонки
                audioFileSection.style.display = 'block';
                smsSection.style.display = 'none';
            } else if (type === 'sms') {
                // Только СМС
                audioFileSection.style.display = 'none';
                smsSection.style.display = 'block';
                // Для SMS кампании скрываем опции "при недозвоне/успехе"
                smsNoAnswerSection.querySelector('.form-check').style.display = 'none';
                smsSuccessSection.querySelector('.form-check').style.display = 'none';
                // Показываем только текстовые поля
                document.getElementById('smsNoAnswerTextSection').style.display = 'block';
            } else if (type === 'call_and_sms') {
                // Звонки + СМС
                audioFileSection.style.display = 'block';
                smsSection.style.display = 'block';
                // Показываем чекбоксы
                smsNoAnswerSection.querySelector('.form-check').style.display = 'block';
                smsSuccessSection.querySelector('.form-check').style.display = 'block';
            }
        });
    }

    // Обработчики чекбоксов СМС
    const sendSmsOnNoAnswer = document.getElementById('sendSmsOnNoAnswer');
    const sendSmsOnSuccess = document.getElementById('sendSmsOnSuccess');

    if (sendSmsOnNoAnswer) {
        sendSmsOnNoAnswer.addEventListener('change', () => {
            document.getElementById('smsNoAnswerTextSection').style.display =
                sendSmsOnNoAnswer.checked ? 'block' : 'none';
        });
    }

    if (sendSmsOnSuccess) {
        sendSmsOnSuccess.addEventListener('change', () => {
            document.getElementById('smsSuccessTextSection').style.display =
                sendSmsOnSuccess.checked ? 'block' : 'none';
        });
    }

    // Загрузка шаблонов при нажатии на кнопку обновления
    const loadTemplatesNoAnswer = document.getElementById('loadTemplatesNoAnswer');
    const loadTemplatesSuccess = document.getElementById('loadTemplatesSuccess');

    if (loadTemplatesNoAnswer) {
        loadTemplatesNoAnswer.addEventListener('click', () => {
            loadSMSTemplates(null, 'smsNoAnswerTemplate');
        });
    }

    if (loadTemplatesSuccess) {
        loadTemplatesSuccess.addEventListener('click', () => {
            loadSMSTemplates(null, 'smsSuccessTemplate');
        });
    }

    // Обработчики выбора шаблона
    const smsNoAnswerTemplate = document.getElementById('smsNoAnswerTemplate');
    const smsSuccessTemplate = document.getElementById('smsSuccessTemplate');

    if (smsNoAnswerTemplate) {
        smsNoAnswerTemplate.addEventListener('change', () => {
            const selectedOption = smsNoAnswerTemplate.options[smsNoAnswerTemplate.selectedIndex];
            if (selectedOption.dataset.text) {
                document.getElementById('smsNoAnswerText').value = selectedOption.dataset.text;
            }
        });
    }

    if (smsSuccessTemplate) {
        smsSuccessTemplate.addEventListener('change', () => {
            const selectedOption = smsSuccessTemplate.options[smsSuccessTemplate.selectedIndex];
            if (selectedOption.dataset.text) {
                document.getElementById('smsSuccessText').value = selectedOption.dataset.text;
            }
        });
    }

    // Сохранение шаблонов
    const saveTemplateNoAnswer = document.getElementById('saveTemplateNoAnswer');
    const saveTemplateSuccess = document.getElementById('saveTemplateSuccess');

    if (saveTemplateNoAnswer) {
        saveTemplateNoAnswer.addEventListener('click', async () => {
            const text = document.getElementById('smsNoAnswerText').value.trim();
            if (!text) {
                showNotification('Введите текст СМС для сохранения', 'warning');
                return;
            }
            const name = prompt('Введите название шаблона:');
            if (name) {
                await saveSMSTemplate(name, text, 'no_answer');
            }
        });
    }

    if (saveTemplateSuccess) {
        saveTemplateSuccess.addEventListener('click', async () => {
            const text = document.getElementById('smsSuccessText').value.trim();
            if (!text) {
                showNotification('Введите текст СМС для сохранения', 'warning');
                return;
            }
            const name = prompt('Введите название шаблона:');
            if (name) {
                await saveSMSTemplate(name, text, 'success');
            }
        });
    }
});

// Загрузка шаблонов СМС
async function loadSMSTemplates(category, selectId) {
    try {
        // Загружаем ВСЕ шаблоны, без фильтрации по категории
        const url = `${API_BASE}/sms/templates`;
        const response = await fetch(url);
        const data = await response.json();

        const select = document.getElementById(selectId);
        if (!select) return; // Если элемент не найден - выходим

        // Очищаем и добавляем опцию по умолчанию
        select.innerHTML = '<option value="">-- Выберите шаблон --</option>';

        if (data.templates && data.templates.length > 0) {
            data.templates.forEach(template => {
                const option = document.createElement('option');
                option.value = template.id;
                option.textContent = template.name;
                option.dataset.text = template.text;
                select.appendChild(option);
            });
            // Убрали уведомления - они надоедают
        }
    } catch (error) {
        console.error('Ошибка загрузки шаблонов:', error);
    }
}

// Сохранение шаблона СМС
async function saveSMSTemplate(name, text, category) {
    try {
        const response = await fetch(`${API_BASE}/sms/templates`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                text,
                category
            })
        });

        if (response.ok) {
            showNotification('Шаблон сохранен!', 'success');

            // Автоматически перезагружаем оба dropdown после сохранения
            await loadSMSTemplates(null, 'smsNoAnswerTemplate');
            await loadSMSTemplates(null, 'smsSuccessTemplate');
        } else {
            throw new Error('Ошибка сохранения шаблона');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Ошибка сохранения шаблона', 'danger');
    }
}

// ============================================
// Вспомогательные функции
// ============================================

function getStatusColor(status) {
    const colors = {
        'draft': 'info',
        'running': 'success',
        'paused': 'warning',
        'completed': 'secondary'
    };
    return colors[status] || 'secondary';
}

function getStatusText(status) {
    const texts = {
        'draft': 'Черновик',
        'running': 'Активна',
        'paused': 'Пауза',
        'completed': 'Завершена'
    };
    return texts[status] || status;
}

// ============================================
// Автообновление данных
// ============================================

// Обновление каждые 5 секунд
setInterval(() => {
    loadSimCards();

    // Если открыта секция с кампаниями - обновляем
    const campaignsSection = document.getElementById('campaignsSection');
    if (campaignsSection.style.display !== 'none') {
        loadCampaigns();
    }
}, 5000);

// ============================================
// Инициализация
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Загружаем начальные данные
    loadCampaigns();
    loadSimCards();
});
