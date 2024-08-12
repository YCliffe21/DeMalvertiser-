import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Adware Detection',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _controller = TextEditingController();
  String _result = '';

  Future<void> _detectAdware() async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/predict'), // Ensure this matches your Flask API endpoint
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: jsonEncode({"features": jsonDecode(_controller.text)}),
      );

      print("Response status: ${response.statusCode}"); // Print status code to debug
      print("Response body: ${response.body}"); // Print response body to debug


      if (response.statusCode == 200) {
        setState(() {
          _result = json.decode(response.body).toString();
        });
      } else {
        setState(() {
          _result = 'Error: ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Adware Detection'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: _controller,
              maxLines: 10,
              decoration: InputDecoration(
                hintText: 'Enter features as JSON array',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: _detectAdware,
              child: Text('Check'),
            ),
            SizedBox(height: 16.0),
            Text(_result),
          ],
        ),
      ),
    );
  }
}
