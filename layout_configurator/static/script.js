// Ensure the grid is created on page load
window.addEventListener("load", createGrid);

let selectedSection = null;
let gridConfig = {
    grid_size: [2, 2],
    sections: [],
    display_settings: {}
};

// Function: Create the outer grid
function createGrid() {
    const rows = parseInt(document.getElementById('gridRows').value);
    const cols = parseInt(document.getElementById('gridCols').value);
    gridConfig.grid_size = [rows, cols];
    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = ''; // Clear container
    gridContainer.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.dataset.position = JSON.stringify([r, c]);
            cell.textContent = 'Drop here';
            cell.addEventListener('dragover', function (e) {
                e.preventDefault();
                this.classList.add('over');
                let source = e.dataTransfer.getData("source");
                e.dataTransfer.dropEffect = (source === "grid") ? "move" : "copy";
            });
            cell.addEventListener('dragleave', function (e) {
                this.classList.remove('over');
            });
            cell.addEventListener('drop', function (e) {
                e.preventDefault();
                this.classList.remove('over');
                let source = e.dataTransfer.getData("source");
                const configData = e.dataTransfer.getData('text/plain');
                if (source === "bank" && configData) {
                    const config = JSON.parse(configData);
                    addSectionToCell(this, config);
                }
            });
            gridContainer.appendChild(cell);
        }
    }
    console.log("Grid created:", rows, "rows x", cols, "cols");
}

// Adds a widget (section) into a grid cell
function addSectionToCell(cell, config) {
    const sectionEl = document.createElement('div');
    sectionEl.className = 'draggable-section dropped';
    sectionEl.draggable = true;
    sectionEl.dataset.config = JSON.stringify(config);
    sectionEl.textContent = config.type || "Empty";
    if (config.size) { sectionEl.classList.add(`size-${config.size}`); }
    if (cell.textContent.trim() === 'Drop here') { cell.innerHTML = ''; }
    cell.appendChild(sectionEl);

    sectionEl.addEventListener('dragstart', function (e) {
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', this.dataset.config);
        e.dataTransfer.setData('source', 'grid');
        this.classList.add('dragging');
    });
    sectionEl.addEventListener('dragover', function (e) {
        e.preventDefault();
        this.classList.add('over');
    });
    sectionEl.addEventListener('dragleave', function (e) {
        this.classList.remove('over');
    });
    sectionEl.addEventListener('drop', function (e) {
        e.preventDefault();
        this.classList.remove('over');
        const dragged = document.querySelector('.dragging');
        if (dragged && dragged !== this) {
            this.parentElement.insertBefore(dragged, this);
        }
    });
    sectionEl.addEventListener('dragend', function (e) {
        this.classList.remove('dragging');
    });
    sectionEl.addEventListener('dblclick', function (e) {
        selectedSection = this;
        showEditPanel(selectedSection);
    });

    if (config.type === "portfolio") {
        let portfolioContainer = document.createElement('div');
        portfolioContainer.className = 'portfolio-inner';

        let topRow = document.createElement('div');
        topRow.className = 'portfolio-top';
        topRow.style.display = "flex";
        topRow.style.justifyContent = "space-between";
        topRow.style.borderBottom = "2px solid #ccc";
        topRow.style.paddingBottom = "8px";
        let leftCol = document.createElement('div');
        leftCol.className = 'portfolio-column';
        leftCol.style.flex = "1";
        leftCol.style.marginRight = "10px";
        leftCol.style.borderRight = "1px solid #ccc";
        let rightCol = document.createElement('div');
        rightCol.className = 'portfolio-column';
        rightCol.style.flex = "1";

        let widgetLeft = document.createElement('div');
        widgetLeft.className = 'sub-widget';
        widgetLeft.textContent = "adabalance";
        addSubWidgetDragEvents(widgetLeft, leftCol);
        leftCol.appendChild(widgetLeft);
        let widgetRight = document.createElement('div');
        widgetRight.className = 'sub-widget';
        widgetRight.textContent = "adavalue";
        addSubWidgetDragEvents(widgetRight, rightCol);
        rightCol.appendChild(widgetRight);

        topRow.appendChild(leftCol);
        topRow.appendChild(rightCol);

        let bottomRow = document.createElement('div');
        bottomRow.className = 'portfolio-bottom';
        bottomRow.style.display = "flex";
        bottomRow.style.flexDirection = "column";
        bottomRow.style.alignItems = "flex-start";
        bottomRow.style.borderTop = "2px solid #ccc";
        bottomRow.style.paddingTop = "8px";
        let bottomWidgets = ["tokens", "lppos", "chart", "trades"];
        bottomWidgets.forEach(widget => {
            let widgetEl = document.createElement('div');
            widgetEl.className = 'sub-widget';
            widgetEl.textContent = widget;
            addSubWidgetDragEvents(widgetEl, bottomRow);
            bottomRow.appendChild(widgetEl);
        });

        portfolioContainer.appendChild(topRow);
        portfolioContainer.appendChild(bottomRow);
        sectionEl.appendChild(portfolioContainer);

        let manageBtn = document.createElement('button');
        manageBtn.className = 'edit-sub-widgets';
        manageBtn.textContent = "Edit";
        manageBtn.style.marginTop = "5px";
        manageBtn.onclick = function (e) {
            e.stopPropagation();
            manageBtn.classList.add('hidden'); // Button ausblenden
            openPortfolioManager(sectionEl, config, portfolioContainer);
        };
        sectionEl.appendChild(manageBtn);
    } else if (config.type === "tokens") {
        let tokenContainer = document.createElement('div');
        tokenContainer.className = 'token-inner';
        tokenContainer.style.display = "flex";
        tokenContainer.style.flexDirection = "row";
        tokenContainer.style.gap = "10px";
        let tokenWidgets = ["logo", "price", "change", "chart"];
        tokenWidgets.forEach(widget => {
            let widgetEl = document.createElement('div');
            widgetEl.className = 'sub-widget';
            widgetEl.textContent = widget;
            addSubWidgetDragEvents(widgetEl, tokenContainer);
            tokenContainer.appendChild(widgetEl);
        });
        sectionEl.appendChild(tokenContainer);

        let manageBtn = document.createElement('button');
        manageBtn.className = 'edit-sub-widgets';
        manageBtn.textContent = "Edit";
        manageBtn.style.marginTop = "5px";
        manageBtn.onclick = function (e) {
            e.stopPropagation();
            manageBtn.classList.add('hidden'); // Button ausblenden
            openTokenManager(sectionEl, config, tokenContainer);
        };
        sectionEl.appendChild(manageBtn);
    } else if (config.type === "market_data") {
        let marketDataContainer = document.createElement('div');
        marketDataContainer.className = 'token-inner';
        marketDataContainer.style.display = "flex";
        marketDataContainer.style.flexDirection = "row";
        marketDataContainer.style.gap = "10px";
        let marketWidgets = config.innerWidgets || ["quote", "activeaddresses", "dexvolume"];
        marketWidgets.forEach(widget => {
            let widgetEl = document.createElement('div');
            widgetEl.className = 'sub-widget';
            widgetEl.textContent = widget;
            addSubWidgetDragEvents(widgetEl, marketDataContainer);
            marketDataContainer.appendChild(widgetEl);
        });
        sectionEl.appendChild(marketDataContainer);

        let manageBtn = document.createElement('button');
        manageBtn.className = 'edit-sub-widgets';
        manageBtn.textContent = "Edit";
        manageBtn.style.marginTop = "5px";
        manageBtn.onclick = function (e) {
            e.stopPropagation();
            manageBtn.classList.add('hidden'); // Button ausblenden
            openMarketDataManager(sectionEl, config, marketDataContainer);
        };
        sectionEl.appendChild(manageBtn);
    } else if (config.type === "nested_grid" || config.type === "center_split") {
        let gridElement = document.createElement('div');
        gridElement.className = 'nested-grid';
        if (config.type === "center_split") {
            gridElement.style.gridTemplateColumns = "repeat(2, 1fr)";
            for (let i = 0; i < 2; i++) {
                let cell = document.createElement('div');
                cell.className = 'nested-grid-cell';
                cell.textContent = "Drop here";
                cell.addEventListener('dragover', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.classList.add('over');
                    let source = e.dataTransfer.getData("source");
                    e.dataTransfer.dropEffect = (source === "bank") ? "copy" : "move";
                });
                cell.addEventListener('dragleave', function (e) {
                    e.stopPropagation();
                    this.classList.remove('over');
                });
                cell.addEventListener('drop', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.classList.remove('over');
                    let source = e.dataTransfer.getData("source");
                    const configData = e.dataTransfer.getData("text/plain");
                    if (source === "bank" && configData) {
                        const labelElem = document.createElement('div');
                        labelElem.className = 'grid-label size-small';
                        const labelConfig = JSON.parse(configData);
                        labelElem.textContent = labelConfig.type || "Label";
                        addGridLabelDragEvents(labelElem, this);
                        this.innerHTML = "";
                        this.appendChild(labelElem);
                    } else {
                        const dragged = document.querySelector('.dragging');
                        if (dragged) {
                            this.innerHTML = "";
                            this.appendChild(dragged);
                        }
                    }
                });
                gridElement.appendChild(cell);
            }
        } else {
            let rows = (config.grid_size && config.grid_size[0]) ? config.grid_size[0] : 2;
            let cols = (config.grid_size && config.grid_size[1]) ? config.grid_size[1] : 2;
            gridElement.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
            for (let i = 0; i < rows * cols; i++) {
                let cell = document.createElement('div');
                cell.className = 'nested-grid-cell';
                cell.textContent = "Drop here";
                cell.addEventListener('dragover', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.classList.add('over');
                    let source = e.dataTransfer.getData("source");
                    e.dataTransfer.dropEffect = (source === "bank") ? "copy" : "move";
                });
                cell.addEventListener('dragleave', function (e) {
                    e.stopPropagation();
                    this.classList.remove('over');
                });
                cell.addEventListener('drop', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.classList.remove('over');
                    let source = e.dataTransfer.getData("source");
                    const configData = e.dataTransfer.getData("text/plain");
                    if (source === "bank" && configData) {
                        const labelElem = document.createElement('div');
                        labelElem.className = 'grid-label size-small';
                        const labelConfig = JSON.parse(configData);
                        labelElem.textContent = labelConfig.type || "Label";
                        addGridLabelDragEvents(labelElem, this);
                        this.innerHTML = "";
                        this.appendChild(labelElem);
                    } else {
                        const dragged = document.querySelector('.dragging');
                        if (dragged) {
                            this.innerHTML = "";
                            this.appendChild(dragged);
                        }
                    }
                });
                gridElement.appendChild(cell);
            }
        }
        sectionEl.appendChild(gridElement);
    }
}

// Internal Drag & Drop Logic for Portfolio/Token/MarketData sub-widgets (MOVE only)
function addSubWidgetDragEvents(widgetEl, container) {
    widgetEl.draggable = true;
    widgetEl.addEventListener('dragstart', function (e) {
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', this.textContent.replace('×', '').trim());
        this.classList.add('dragging');
    });
    widgetEl.addEventListener('dragend', function (e) {
        this.classList.remove('dragging');
    });
    container.addEventListener('dragover', function (e) {
        e.preventDefault();
        container.classList.add('over');
        e.dataTransfer.dropEffect = 'move';
    });
    container.addEventListener('dragleave', function (e) {
        container.classList.remove('over');
    });
    container.addEventListener('drop', function (e) {
        e.preventDefault();
        container.classList.remove('over');
        const draggedElem = Array.from(container.children).find(child => child.classList.contains('dragging'));
        if (draggedElem) {
            container.insertBefore(draggedElem, e.target.closest('.sub-widget'));
        }
    });
    if (!widgetEl.querySelector('.delete-btn')) {
        let deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = '×';
        deleteBtn.onclick = function (e) {
            e.stopPropagation();
            widgetEl.remove();
        };
        widgetEl.appendChild(deleteBtn);
    }
}

// New Drag & Drop Logic for Grid Labels in Nested Grids
function addGridLabelDragEvents(labelEl, container) {
    labelEl.draggable = true;
    let deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn';
    deleteBtn.textContent = '×';
    deleteBtn.onclick = function (e) {
        e.stopPropagation();
        labelEl.remove();
    };
    labelEl.appendChild(deleteBtn);
    labelEl.addEventListener('dragstart', function (e) {
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', this.textContent.replace('×', '').trim());
        this.classList.add('dragging');
    });
    labelEl.addEventListener('dragend', function (e) {
        this.classList.remove('dragging');
    });
    container.addEventListener('dragover', function (e) {
        e.preventDefault();
        container.classList.add('over');
        e.dataTransfer.dropEffect = 'move';
    });
    container.addEventListener('dragleave', function (e) {
        container.classList.remove('over');
    });
    container.addEventListener('drop', function (e) {
        e.preventDefault();
        container.classList.remove('over');
        const draggedElem = Array.from(container.children).find(child => child.classList.contains('dragging'));
        if (draggedElem) {
            container.insertBefore(draggedElem, e.target.closest('.grid-label'));
        }
    });
}

// Global function: Open the management interface for Portfolio sub-widgets
function openPortfolioManager(sectionEl, config, portfolioContainer) {
    if (sectionEl.querySelector('.portfolio-manager')) return;
    let managerPanel = document.createElement('div');
    managerPanel.className = 'portfolio-manager';
    managerPanel.innerHTML = "<h3>Manage Sub-Widgets</h3>";
    let ul = document.createElement('ul');
    ul.className = "manage-list";
    const allPortfolioWidgets = ["adabalance", "adavalue", "tokens", "lppos", "chart", "trades"];
    allPortfolioWidgets.forEach(widget => {
        let li = document.createElement('li');
        li.draggable = true;
        li.textContent = widget;
        let checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.checked = config.innerWidgets && config.innerWidgets.includes(widget);
        li.prepend(checkbox);
        li.addEventListener('dragstart', function (e) {
            e.dataTransfer.setData('text/plain', widget);
            li.classList.add('dragging');
        });
        li.addEventListener('dragend', function (e) {
            li.classList.remove('dragging');
        });
        li.addEventListener('dragover', function (e) {
            e.preventDefault();
            li.classList.add('over');
        });
        li.addEventListener('dragleave', function (e) {
            li.classList.remove('over');
        });
        li.addEventListener('drop', function (e) {
            e.preventDefault();
            li.classList.remove('over');
            let draggedWidget = e.dataTransfer.getData('text/plain');
            li.textContent = draggedWidget;
            li.prepend(checkbox);
        });
        ul.appendChild(li);
    });
    managerPanel.appendChild(ul);
    let saveBtn = document.createElement('button');
    saveBtn.textContent = "Save";
    saveBtn.onclick = function (e) {
        let newOrder = [];
        ul.querySelectorAll("li").forEach(li => {
            let widgetName = li.textContent.trim();
            let cb = li.querySelector("input[type='checkbox']");
            if (cb && cb.checked) {
                newOrder.push(widgetName);
            }
        });
        config.innerWidgets = newOrder;
        let newContainer = document.createElement('div');
        newContainer.className = 'portfolio-inner';
        let topRow = document.createElement('div');
        topRow.className = 'portfolio-top';
        topRow.style.display = "flex";
        topRow.style.justifyContent = "space-between";
        let leftCol = document.createElement('div');
        leftCol.className = 'portfolio-column';
        leftCol.style.flex = "1";
        leftCol.style.marginRight = "10px";
        let rightCol = document.createElement('div');
        rightCol.className = 'portfolio-column';
        rightCol.style.flex = "1";
        let topWidgets = ["adabalance", "adavalue"];
        topWidgets.forEach(widget => {
            if (newOrder.includes(widget)) {
                let widgetEl = document.createElement('div');
                widgetEl.className = 'sub-widget';
                widgetEl.textContent = widget;
                addSubWidgetDragEvents(widgetEl, leftCol);
                leftCol.appendChild(widgetEl);
            }
        });
        topRow.appendChild(leftCol);
        topRow.appendChild(rightCol);
        let bottomRow = document.createElement('div');
        bottomRow.className = 'portfolio-bottom';
        bottomRow.style.display = "flex";
        bottomRow.style.flexDirection = "column";
        bottomRow.style.alignItems = "flex-start";
        let remaining = newOrder.filter(w => !topWidgets.includes(w));
        remaining.forEach(widget => {
            let widgetEl = document.createElement('div');
            widgetEl.className = 'sub-widget';
            widgetEl.textContent = widget;
            addSubWidgetDragEvents(widgetEl, bottomRow);
            bottomRow.appendChild(widgetEl);
        });
        newContainer.appendChild(topRow);
        newContainer.appendChild(bottomRow);
        let oldContainer = sectionEl.querySelector('.portfolio-inner');
        if (oldContainer) { oldContainer.remove(); }
        sectionEl.insertBefore(newContainer, sectionEl.querySelector('.edit-sub-widgets'));
        managerPanel.remove();
        sectionEl.querySelector('.edit-sub-widgets').classList.remove('hidden'); // Button wieder einblenden
        sectionEl.dataset.config = JSON.stringify(config);
    };
    let cancelBtn = document.createElement('button');
    cancelBtn.textContent = "Cancel";
    cancelBtn.onclick = function (e) {
        managerPanel.remove();
        sectionEl.querySelector('.edit-sub-widgets').classList.remove('hidden'); // Button wieder einblenden
    };
    managerPanel.appendChild(saveBtn);
    managerPanel.appendChild(cancelBtn);
    sectionEl.appendChild(managerPanel);
}

// Global function: Open the management interface for Token sub-widgets (including tickers)
// Global function: Open the management interface for Token sub-widgets (including tickers)
function openTokenManager(sectionEl, config, tokenContainer) {
    if (sectionEl.querySelector('.token-manager')) return;
    let managerPanel = document.createElement('div');
    managerPanel.className = 'token-manager';
    managerPanel.innerHTML = "<h3>Manage Sub-Widgets</h3>";
    let ul = document.createElement('ul');
    ul.className = "manage-list";
    const allTokenWidgets = ["logo", "price", "change", "chart"];
    allTokenWidgets.forEach(widget => {
        let li = document.createElement('li');
        li.draggable = true;
        li.textContent = widget;
        let checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.checked = config.show && config.show.includes(widget); // Verwende config.show statt innerWidgets
        li.prepend(checkbox);
        li.addEventListener('dragstart', function (e) {
            e.dataTransfer.setData('text/plain', widget);
            li.classList.add('dragging');
        });
        li.addEventListener('dragend', function (e) {
            li.classList.remove('dragging');
        });
        li.addEventListener('dragover', function (e) {
            e.preventDefault();
            li.classList.add('over');
        });
        li.addEventListener('dragleave', function (e) {
            li.classList.remove('over');
        });
        li.addEventListener('drop', function (e) {
            e.preventDefault();
            li.classList.remove('over');
            let draggedWidget = e.dataTransfer.getData('text/plain');
            li.textContent = draggedWidget;
            li.prepend(checkbox);
        });
        ul.appendChild(li);
    });
    managerPanel.appendChild(ul);
    let tickerDiv = document.createElement('div');
    tickerDiv.style.marginTop = "10px";
    let tickerLabel = document.createElement('label');
    tickerLabel.textContent = "Tickers (comma separated):";
    let tickerInput = document.createElement('input');
    tickerInput.type = "text";
    tickerInput.style.width = "100%";
    tickerInput.style.marginTop = "5px";
    if (config.tokens && Array.isArray(config.tokens)) {
        tickerInput.value = config.tokens.join(", ");
    }
    tickerDiv.appendChild(tickerLabel);
    tickerDiv.appendChild(tickerInput);
    managerPanel.appendChild(tickerDiv);
    let saveBtn = document.createElement('button');
    saveBtn.textContent = "Save Sub-Widget Settings";
    saveBtn.onclick = function (e) {
        let newOrder = [];
        ul.querySelectorAll("li").forEach(li => {
            let widgetName = li.textContent.trim();
            let cb = li.querySelector("input[type='checkbox']");
            if (cb && cb.checked) {
                newOrder.push(widgetName);
            }
        });
        config.innerWidgets = newOrder; // Speichere als innerWidgets für Konsistenz
        if (tickerInput.value.trim() !== "") {
            config.tokens = tickerInput.value.split(",").map(t => t.trim());
        } else {
            config.tokens = [];
        }
        let newContainer = document.createElement('div');
        newContainer.className = 'token-inner';
        newContainer.style.display = "flex";
        newContainer.style.flexDirection = "row";
        newContainer.style.gap = "10px";
        allTokenWidgets.forEach(widget => {
            if (newOrder.includes(widget)) {
                let widgetEl = document.createElement('div');
                widgetEl.className = 'sub-widget';
                widgetEl.textContent = widget;
                addSubWidgetDragEvents(widgetEl, newContainer);
                newContainer.appendChild(widgetEl);
            }
        });
        let oldContainer = sectionEl.querySelector('.token-inner');
        if (oldContainer) { oldContainer.remove(); }
        sectionEl.insertBefore(newContainer, sectionEl.querySelector('.edit-sub-widgets'));
        managerPanel.remove();
        sectionEl.querySelector('.edit-sub-widgets').classList.remove('hidden');
        sectionEl.dataset.config = JSON.stringify(config);
    };
    let cancelBtn = document.createElement('button');
    cancelBtn.textContent = "Cancel";
    cancelBtn.onclick = function (e) {
        managerPanel.remove();
        sectionEl.querySelector('.edit-sub-widgets').classList.remove('hidden');
    };
    managerPanel.appendChild(saveBtn);
    managerPanel.appendChild(cancelBtn);
    sectionEl.appendChild(managerPanel);
}

// Global function: Open the management interface for Market Data sub-widgets
function openMarketDataManager(sectionEl, config, marketDataContainer) {
    if (sectionEl.querySelector('.market-data-manager')) return;
    let managerPanel = document.createElement('div');
    managerPanel.className = 'market-data-manager';
    managerPanel.innerHTML = "<h3>Manage Sub-Widgets</h3>";
    let ul = document.createElement('ul');
    ul.className = "manage-list";
    const allMarketWidgets = ["quote", "activeaddresses", "dexvolume"];
    allMarketWidgets.forEach(widget => {
        let li = document.createElement('li');
        li.draggable = true;
        li.textContent = widget;
        let checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.checked = config.innerWidgets && config.innerWidgets.includes(widget);
        li.prepend(checkbox);
        li.addEventListener('dragstart', function (e) {
            e.dataTransfer.setData('text/plain', widget);
            li.classList.add('dragging');
        });
        li.addEventListener('dragend', function (e) {
            li.classList.remove('dragging');
        });
        li.addEventListener('dragover', function (e) {
            e.preventDefault();
            li.classList.add('over');
        });
        li.addEventListener('dragleave', function (e) {
            li.classList.remove('over');
        });
        li.addEventListener('drop', function (e) {
            e.preventDefault();
            li.classList.remove('over');
            let draggedWidget = e.dataTransfer.getData('text/plain');
            li.textContent = draggedWidget;
            li.prepend(checkbox);
        });
        ul.appendChild(li);
    });
    managerPanel.appendChild(ul);
    let saveBtn = document.createElement('button');
    saveBtn.textContent = "Save";
    saveBtn.onclick = function (e) {
        let newOrder = [];
        ul.querySelectorAll("li").forEach(li => {
            let widgetName = li.textContent.trim();
            let cb = li.querySelector("input[type='checkbox']");
            if (cb && cb.checked) {
                newOrder.push(widgetName);
            }
        });
        config.innerWidgets = newOrder;
        let newContainer = document.createElement('div');
        newContainer.className = 'token-inner';
        newContainer.style.display = "flex";
        newContainer.style.flexDirection = "row";
        newContainer.style.gap = "10px";
        allMarketWidgets.forEach(widget => {
            if (newOrder.includes(widget)) {
                let widgetEl = document.createElement('div');
                widgetEl.className = 'sub-widget';
                widgetEl.textContent = widget;
                addSubWidgetDragEvents(widgetEl, newContainer);
                newContainer.appendChild(widgetEl);
            }
        });
        let oldContainer = sectionEl.querySelector('.token-inner');
        if (oldContainer) { oldContainer.remove(); }
        sectionEl.insertBefore(newContainer, sectionEl.querySelector('.edit-sub-widgets'));
        managerPanel.remove();
        sectionEl.querySelector('.edit-sub-widgets').classList.remove('hidden'); // Button wieder einblenden
        sectionEl.dataset.config = JSON.stringify(config);
    };
    let cancelBtn = document.createElement('button');
    cancelBtn.textContent = "Cancel";
    cancelBtn.onclick = function (e) {
        managerPanel.remove();
        sectionEl.querySelector('.edit-sub-widgets').classList.remove('hidden'); // Button wieder einblenden
    };
    managerPanel.appendChild(saveBtn);
    managerPanel.appendChild(cancelBtn);
    sectionEl.appendChild(managerPanel);
}

// Edit Panel for General Properties
function showEditPanel(sectionEl) {
    const config = JSON.parse(sectionEl.dataset.config);
    document.getElementById('edit-type').value = config.type || "";
    document.getElementById('edit-font_size').value = config.font_size || "";
    document.getElementById('edit-color').value = config.color || "";
    document.getElementById('edit-size').value = config.size || "medium";
    document.getElementById('edit-panel').style.display = 'block';
}
function saveEdit() {
    if (!selectedSection) return;
    const config = JSON.parse(selectedSection.dataset.config);
    config.type = document.getElementById('edit-type').value;
    config.font_size = parseInt(document.getElementById('edit-font_size').value);
    config.color = document.getElementById('edit-color').value;
    config.size = document.getElementById('edit-size').value;
    selectedSection.dataset.config = JSON.stringify(config);
    selectedSection.textContent = config.type || "Empty";
    if (config.type === "portfolio") {
        const portfolioContainer = selectedSection.querySelector('.portfolio-inner');
        if (portfolioContainer) {
            selectedSection.appendChild(portfolioContainer);
        }
    }
    document.getElementById('edit-panel').style.display = 'none';
}
function cancelEdit() {
    document.getElementById('edit-panel').style.display = 'none';
    selectedSection = null;
}

// Trash Zone: The Section Bank serves as the trash zone – widgets already in the grid are removed when dropped here.
const sectionBankEl = document.getElementById('section-bank');
sectionBankEl.addEventListener('dragover', function (e) {
    e.preventDefault();
    this.classList.add('over');
    e.dataTransfer.dropEffect = 'move';
});
sectionBankEl.addEventListener('dragleave', function (e) {
    this.classList.remove('over');
});
sectionBankEl.addEventListener('drop', function (e) {
    e.preventDefault();
    this.classList.remove('over');
    const dragged = document.querySelector('.dragging');
    if (dragged && dragged.classList.contains('dropped')) {
        dragged.remove();
    }
});

// Drag & Drop for Section Bank items (prototypes)
document.querySelectorAll('.section-bank .section-item').forEach(item => {
    item.addEventListener('dragstart', function (e) {
        e.dataTransfer.setData('text/plain', this.dataset.config);
        e.dataTransfer.setData('source', 'bank');
        this.classList.add('dragging');
    });
    item.addEventListener('dragend', function () {
        this.classList.remove('dragging');
    });
});

// Exports the configuration as JSON (including sub-widgets)
function exportConfig() {
    const gridContainer = document.getElementById('grid-container');
    const cells = gridContainer.querySelectorAll('.grid-cell');
    const sections = [];
    cells.forEach(cell => {
        const cellSections = cell.querySelectorAll('.draggable-section');
        cellSections.forEach(section => {
            const config = JSON.parse(section.dataset.config);
            const position = JSON.parse(cell.dataset.position);
            if (config.type === "portfolio") {
                const portfolioContainer = section.querySelector('.portfolio-inner');
                if (portfolioContainer) {
                    let widgets = [];
                    Array.from(portfolioContainer.querySelectorAll('.sub-widget')).forEach(child => {
                        widgets.push(child.childNodes[0] ? child.childNodes[0].nodeValue.trim() : "");
                    });
                    config.innerWidgets = widgets;
                }
            }
            if (config.type === "tokens") {
                const tokenContainer = section.querySelector('.token-inner');
                if (tokenContainer) {
                    let widgets = [];
                    Array.from(tokenContainer.querySelectorAll('.sub-widget')).forEach(child => {
                        widgets.push(child.childNodes[0] ? child.childNodes[0].nodeValue.trim() : "");
                    });
                    config.innerWidgets = widgets;
                }
            }
            if (config.type === "market_data") {
                const marketDataContainer = section.querySelector('.token-inner');
                if (marketDataContainer) {
                    let widgets = [];
                    Array.from(marketDataContainer.querySelectorAll('.sub-widget')).forEach(child => {
                        widgets.push(child.childNodes[0] ? child.childNodes[0].nodeValue.trim() : "");
                    });
                    config.innerWidgets = widgets;
                }
            }
            if (config.type === "nested_grid" || config.type === "center_split") {
                const gridElement = section.querySelector('.nested-grid');
                if (gridElement) {
                    let cellsArr = [];
                    Array.from(gridElement.children).forEach(cell => {
                        let labelElem = cell.querySelector('.grid-label');
                        cellsArr.push(labelElem ? labelElem.childNodes[0].nodeValue.trim() : "");
                    });
                    config.cells = cellsArr;
                }
            }
            config.position = position;
            sections.push(config);
        });
    });
    gridConfig.sections = sections;
    const output = JSON.stringify(gridConfig, null, 4);
    document.getElementById('exported-json').textContent = output;
}

// Create the grid on page load
createGrid();