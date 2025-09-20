"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Badge } from "@/components/ui/badge"

// Simulación de una base de datos de usuarios
const users = [
  { id: 1, name: "Alice Johnson", username: "alice_j" },
  { id: 2, name: "Bob Smith", username: "bob_smith" },
  { id: 3, name: "Carol Williams", username: "carol_w" },
  { id: 4, name: "David Brown", username: "david_b" },
  { id: 5, name: "Eva Davis", username: "eva_d" },
  // Añade más usuarios aquí...
]

export default function UserSelect() {
  const [open, setOpen] = React.useState(false)
  const [selectedUsers, setSelectedUsers] = React.useState<typeof users>([])
  const [searchValue, setSearchValue] = React.useState("")

  const filteredUsers = users.filter((user) =>
    `${user.name} ${user.username}`.toLowerCase().includes(searchValue.toLowerCase()),
  )

  const toggleUser = (user: (typeof users)[number]) => {
    setSelectedUsers((current) =>
      current.some((u) => u.id === user.id) ? current.filter((u) => u.id !== user.id) : [...current, user],
    )
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" role="combobox" aria-expanded={open} className="w-full justify-between">
          {selectedUsers.length > 0
            ? `${selectedUsers.length} usuario${
                selectedUsers.length !== 1 ? "s" : ""
              } seleccionado${selectedUsers.length !== 1 ? "s" : ""}`
            : "Seleccionar usuarios..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0">
        <Command>
          <CommandInput placeholder="Buscar usuarios..." value={searchValue} onValueChange={setSearchValue} />
          <CommandList>
            <CommandEmpty>No se encontraron usuarios.</CommandEmpty>
            <CommandGroup className="max-h-64 overflow-y-auto">
              {filteredUsers.map((user) => (
                <CommandItem
                  key={user.id}
                  onSelect={() => toggleUser(user)}
                  className="flex items-center justify-between"
                >
                  <span>
                    {user.name} <span className="text-sm text-muted-foreground">(@{user.username})</span>
                  </span>
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      selectedUsers.some((u) => u.id === user.id) ? "opacity-100" : "opacity-0",
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
      <div className="mt-2 flex flex-wrap gap-2">
        {selectedUsers.map((user) => (
          <Badge key={user.id} variant="secondary" className="flex items-center gap-1">
            {user.name}
            <button
              className="ml-1 rounded-full outline-none focus:ring-2 focus:ring-offset-2"
              onClick={() => toggleUser(user)}
            >
              ×
            </button>
          </Badge>
        ))}
      </div>
    </Popover>
  )
}
