package com.example.simplenotes

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import android.widget.Toast
import com.example.simplenotes.ui.theme.SimpleNotesTheme
import java.io.IOException

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SimpleNotesTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    NotesApp()
                }
            }
        }
    }
}

data class Note(
    val id: Int,
    val title: String,
    val content: String,
    val timestamp: Long = System.currentTimeMillis()
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotesApp() {
    var title by remember { mutableStateOf("") }
    var content by remember { mutableStateOf("") }
    val notes = remember { mutableStateListOf<Note>() }
    var nextId by remember { mutableStateOf(1) }
    var showDeleteDialog by remember { mutableStateOf(false) }
    var noteToDelete by remember { mutableStateOf<Note?>(null) }
    val context = LocalContext.current
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Заголовок приложения
        Text(
            text = "Заметки",
            style = MaterialTheme.typography.headlineSmall
        )

        // Разделитель
        Divider()

        // Поле для заголовка заметки
        OutlinedTextField(
            value = title,
            onValueChange = { title = it },
            label = { Text("Заголовок заметки") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        // Поле для содержания заметки
        OutlinedTextField(
            value = content,
            onValueChange = { content = it },
            label = { Text("Текст заметки") },
            modifier = Modifier
                .fillMaxWidth()
                .height(120.dp),
            maxLines = 4
        )

        // Кнопка сохранения
        Button(
            onClick = {
                if (title.isNotBlank() && content.isNotBlank()) {
                    notes.add(Note(nextId, title, content))
                    nextId++
                    title = ""
                    content = ""
                    Toast.makeText(context, "Заметка сохранена!", Toast.LENGTH_SHORT).show()
                }
            },
            modifier = Modifier.align(Alignment.End),
            enabled = title.isNotBlank() && content.isNotBlank()
        ) {
            Text("Сохранить заметку")
        }

        // Разделитель
        Divider()

        // Список заметок
        Text(
            text = "Сохраненные заметки (${notes.size}):",
            style = MaterialTheme.typography.titleMedium
        )

        if (notes.isEmpty()) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "Заметок пока нет",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Создайте первую заметку для тестирования",
                    style = MaterialTheme.typography.bodySmall
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(max = 400.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(
                    items = notes,
                    key = { it.id }
                ) { note ->
                    NoteCard(
                        note = note,
                        onDelete = {
                            noteToDelete = note
                            showDeleteDialog = true
                        },
                        onInfo = {
                            Toast.makeText(
                                context,
                                "Заметка создана: ${android.text.format.DateFormat.format("dd.MM.yyyy HH:mm", note.timestamp)}",
                                Toast.LENGTH_LONG
                            ).show()
                        }
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(32.dp))
    }

    // Диалог подтверждения удаления
    if (showDeleteDialog) {
        AlertDialog(
            onDismissRequest = { showDeleteDialog = false },
            title = { Text("Удаление заметки") },
            text = { Text("Вы уверены, что хотите удалить заметку \"${noteToDelete?.title}\"?") },
            confirmButton = {
                TextButton(
                    onClick = {
                        noteToDelete?.let { notes.remove(it) }
                        showDeleteDialog = false
                        Toast.makeText(context, "Заметка удалена", Toast.LENGTH_SHORT).show()
                    }
                ) {
                    Text("Удалить")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = { showDeleteDialog = false }
                ) {
                    Text("Отмена")
                }
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NoteCard(
    note: Note,
    onDelete: () -> Unit,
    onInfo: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = note.title,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = note.content,
                    style = MaterialTheme.typography.bodyMedium
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = android.text.format.DateFormat.format("dd.MM.yyyy HH:mm", note.timestamp).toString(),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            // Кнопки действий
            Row {
                IconButton(
                    onClick = onInfo,
                    modifier = Modifier.size(24.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Info,
                        contentDescription = "Информация",
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(
                    onClick = onDelete,
                    modifier = Modifier.size(24.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "Удалить",
                        tint = MaterialTheme.colorScheme.error
                    )
                }
            }
        }
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 640)
@Composable
fun PortraitPreview() {
    SimpleNotesTheme {
        NotesApp()
    }
}

@Preview(showBackground = true, widthDp = 640, heightDp = 360)
@Composable
fun LandscapePreview() {
    SimpleNotesTheme {
        NotesApp()
    }
}