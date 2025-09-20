function createUserSelect(container, hiddenInput) {
  // Ocultar el select original
  hiddenInput.style.display = "none"

  // Obtener usuarios ya seleccionados (para edición)
  const selectedUsers = new Set(Array.from(hiddenInput.selectedOptions).map((option) => option.value))

  // Crear elementos del componente
  const wrapper = document.createElement("div")
  wrapper.className = "user-select-wrapper"

  const input = document.createElement("input")
  input.type = "text"
  input.placeholder = "Buscar usuarios..."
  input.className = "user-select-input form-control"

  const dropdown = document.createElement("div")
  dropdown.className = "user-select-dropdown"

  const selectedList = document.createElement("div")
  selectedList.className = "user-select-selected"

  // Construir el componente
  wrapper.appendChild(input)
  wrapper.appendChild(dropdown)
  container.appendChild(wrapper)
  container.appendChild(selectedList)

  // Almacenar usuarios cargados
  let users = []
  let isLoading = false

  // Función para actualizar la lista de usuarios seleccionados
  function updateSelectedUsers() {
    selectedList.innerHTML = ""

    // Para cada ID de usuario seleccionado
    selectedUsers.forEach((userId) => {
      const user = users.find((u) => u.id.toString() === userId.toString())
      if (user) {
        const badge = document.createElement("span")
        badge.className = "user-badge"
        badge.textContent = user.display_name

        const removeBtn = document.createElement("button")
        removeBtn.type = "button"
        removeBtn.textContent = "×"
        removeBtn.onclick = (e) => {
          e.preventDefault()
          selectedUsers.delete(userId)
          updateSelectedUsers()
          updateHiddenInput()
        }

        badge.appendChild(removeBtn)
        selectedList.appendChild(badge)
      }
    })
  }

  // Función para actualizar el input oculto con los valores seleccionados
  function updateHiddenInput() {
    // Deseleccionar todas las opciones primero
    Array.from(hiddenInput.options).forEach((option) => {
      option.selected = false
    })

    // Seleccionar solo las opciones correspondientes a los usuarios seleccionados
    selectedUsers.forEach((userId) => {
      const option = hiddenInput.querySelector(`option[value="${userId}"]`)
      if (option) {
        option.selected = true
      }
    })

    // Disparar evento de cambio para que cualquier otro código que escuche cambios en el select se entere
    const event = new Event("change", { bubbles: true })
    hiddenInput.dispatchEvent(event)
  }

  // Función para buscar usuarios
  async function searchUsers(query) {
    if (isLoading) return

    isLoading = true
    dropdown.innerHTML = '<div class="p-2 text-center">Buscando...</div>'

    try {
      // Hacer la petición a la API
      const response = await fetch(`/Investigador/api_usuarios/?search=${encodeURIComponent(query)}`)

      if (!response.ok) {
        throw new Error("Error al buscar usuarios")
      }

      users = await response.json()

      // Actualizar el dropdown
      dropdown.innerHTML = ""

      if (users.length === 0) {
        dropdown.innerHTML = '<div class="p-2 text-center">No se encontraron usuarios</div>'
        return
      }

      users.forEach((user) => {
        const item = document.createElement("div")
        item.className = "user-select-item"

        // Mostrar nombre completo y username
        item.textContent = user.display_name

        // Marcar como seleccionado si ya está en la lista
        if (selectedUsers.has(user.id.toString())) {
          item.classList.add("selected")
          item.style.backgroundColor = "#e9ecef"
        }

        item.onclick = () => {
          if (selectedUsers.has(user.id.toString())) {
            selectedUsers.delete(user.id.toString())
          } else {
            selectedUsers.add(user.id.toString())
          }
          updateSelectedUsers()
          updateHiddenInput()
          item.classList.toggle("selected")
        }

        dropdown.appendChild(item)
      })
    } catch (error) {
      console.error("Error:", error)
      dropdown.innerHTML = '<div class="p-2 text-center text-danger">Error al buscar usuarios</div>'
    } finally {
      isLoading = false
    }
  }

  // Eventos
  input.addEventListener("focus", () => {
    dropdown.style.display = "block"
    if (input.value.trim() === "") {
      searchUsers("")
    }
  })

  input.addEventListener("blur", (e) => {
    // Pequeño retraso para permitir que se detecten clics en el dropdown
    setTimeout(() => {
      dropdown.style.display = "none"
    }, 200)
  })

  input.addEventListener("input", () => {
    const query = input.value.trim()
    searchUsers(query)
  })

  // Inicializar el componente con los usuarios ya seleccionados
  if (selectedUsers.size > 0) {
    // Cargar los usuarios seleccionados para mostrarlos
    fetch(`/Investigador/api_usuarios/?ids=${Array.from(selectedUsers).join(",")}`)
      .then((response) => response.json())
      .then((data) => {
        users = data
        updateSelectedUsers()
      })
      .catch((error) => {
        console.error("Error al cargar usuarios seleccionados:", error)
      })
  }
}
