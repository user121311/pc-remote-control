import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PC Control',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final String baseUrl = 'https://pc-remote-control.onrender.com';
  String connectionStatus = 'Connecting...';
  List<String> activeClients = [];
  String? selectedClientId;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    checkConnection();
    fetchActiveClients();
    _timer = Timer.periodic(const Duration(seconds: 5), (_) {
      fetchActiveClients();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> checkConnection() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/'));
      setState(() {
        connectionStatus = response.statusCode == 200
            ? 'Connected to Server'
            : 'Failed to connect to Server';
      });
    } catch (e) {
      setState(() {
        connectionStatus = 'Error: ${e.toString()}';
      });
    }
  }

  Future<void> fetchActiveClients() async {
  try {
    final response = await http.get(Uri.parse('$baseUrl/active_clients'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final clients = data["active_clients"] as List;

      setState(() {
        activeClients = clients
            .map<String>((client) => client["client_id"] as String)
            .toList();
      });
    }
  } catch (e) {
    print('Error fetching active clients: $e');
  }
}


  Future<void> sendCommand(String command) async {
    if (selectedClientId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a client')),
      );
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/send_command'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'command': command, 'client_id': selectedClientId}),
      );

      if (response.statusCode == 200) {
        print('Command sent successfully');
      } else {
        print('Failed to send command');
      }
    } catch (e) {
      print('Error sending command: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PC Control Server'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(8.0),
              color: connectionStatus == 'Connected to Server'
                  ? Colors.green
                  : Colors.red,
              child: Text(
                connectionStatus,
                style: const TextStyle(color: Colors.white, fontSize: 18),
              ),
            ),
            const SizedBox(height: 20),
            DropdownButton<String>(
              hint: const Text('Select Active Client'),
              value: selectedClientId,
             
              items: activeClients
                  .map((client) =>
                      DropdownMenuItem(value: client, child: Text(client)))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  selectedClientId = value;
                });
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => sendCommand('shutdown'),
              child: const Text('Shutdown PC'),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () => sendCommand('open'),
              child: const Text('Відкрити калькулятор'),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: fetchActiveClients,
              child: const Text('Refresh Active Clients'),
            ),
          ],
        ),
      ),
    );
  }
}
