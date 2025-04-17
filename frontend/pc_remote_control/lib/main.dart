import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PC Control',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key}); // замінити на IP сервера

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final String baseUrl = 'https://pc-remote-control.onrender.com';  // URL вашого сервера

  String connectionStatus = 'Connecting...'; // Статус підключення
// Функція для виклику запиту на додавання нової команди
Future<void> sendCommand(String command) async {
  try {
    final response = await http.post(
     Uri.parse('$baseUrl/send_command'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'command': command}),
    );

    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');

    if (response.statusCode == 200) {
      print('Command sent successfully');
    } else {
      print('Failed to send command');
    }
  } catch (e) {
    print('Error sending command: $e');
    if (e is http.ClientException) {
      print('ClientException details: ${e.message}');
    }
  }
}

  // Функція для виклику запиту на перевірку підключення до сервера
  Future<void> checkConnection() async {
    try {
    final response = await http.get(Uri.parse('$baseUrl/'));

      if (response.statusCode == 200) {
        setState(() {
          connectionStatus = 'Connected to Server';
        });
      } else {
        setState(() {
          connectionStatus = 'Failed to connect to Server';
        });
      }
    } catch (e) {
      setState(() {
        connectionStatus = 'Error: ${e.toString()}';
      });
      throw Exception(e);
    }
  }

  // Функція для виклику запиту на отримання нових команд
  Future<void> getCommands() async {
    try {
      final response = await http.get(Uri.https('$baseUrl', '/get_commands'));

      if (response.statusCode == 200) {
        final List<dynamic> commands = json.decode(response.body);
        if (commands.isNotEmpty) {
          for (var command in commands) {
            print('Received Command: $command');
            // Ваша логіка для обробки команд
            // Наприклад, виклик функції для виконання команди
          }
        } else {
          print('No new commands');
        }
      } else {
        print('Failed to fetch commands');
      }
    } catch (e) {
      print('Error fetching commands: $e');
    }
  }

  // Функція для виклику запиту на відключення комп'ютера
  Future<void> shutdown() async {
    final response = await http.post(
      Uri.parse('$baseUrl/shutdown'),
    );

    if (response.statusCode == 200) {
      print('Shutdown initiated');
    } else {
      print('Failed to shutdown');
    }
  }

  // Функція для виклику запиту на відкриття програми
  Future<void> openApp() async {
    final response = await http.post(
      Uri.parse('$baseUrl/open'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      print('App opened');
    } else {
      print('Failed to open app');
    }
  }

  @override
  void initState() {
    super.initState();
    checkConnection(); // Перевірка підключення при старті програми
    // getCommands(); // Викликаємо перевірку на нові команди
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PC Control Server'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            // Лейбл для статусу підключення
            Container(
              padding: EdgeInsets.all(8.0),
              color: connectionStatus == 'Connected to Server'
                  ? Colors.green
                  : Colors.red,
              child: Text(
                connectionStatus,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => sendCommand('test'),
              child: Text('Shutdown PC'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => sendCommand('open'), // Вкажіть шлях до програми
              child: Text('Open App'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => getCommands(),  // Перевірити нові команди
              child: Text('Check for New Commands'),
            ),
          ],
        ),
      ),
    );
  }
}
