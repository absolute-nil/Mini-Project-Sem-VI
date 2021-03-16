import 'package:flutter/material.dart';
import 'package:handsign/presentation/screen/main_screen.dart';
import 'package:camera/camera.dart';

List<CameraDescription> cameras;

Future<Null> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    cameras = await availableCameras();
  } on CameraException catch (e) {
    print('Error: $e.code\nError Message: $e.message');
  }
  runApp(
    MaterialApp(
      debugShowCheckedModeBanner: false,
      darkTheme: ThemeData.light(),
      home: MainScreen(
        cameras: cameras,
      ),
    ),
  );
}
