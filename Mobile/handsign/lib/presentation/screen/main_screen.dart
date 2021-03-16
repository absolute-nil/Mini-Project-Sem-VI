import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:handsign/core/animations/animated_background.dart';
import 'package:handsign/core/animations/fadein.dart';

class MainScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const MainScreen({Key key, @required this.cameras}) : super(key: key);

  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: AnimatedBackground(
        child: Container(
          child: Scaffold(
            backgroundColor: Colors.transparent,
            body: Center(
              child: CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(
                    child: FadeIn(
                      delay: 10.0,
                      duration: Duration(seconds: 1),
                      child: Container(
                        height: 330,
                        width: 200,
                        child: Image.asset(
                          "assets/app_logo.png",
                          fit: BoxFit.contain,
                        ),
                      ),
                    ),
                  ),
                  SliverToBoxAdapter(
                    child: FadeIn(
                      delay: 12.0,
                      duration: Duration(seconds: 1),
                      child: Container(
                        height: 50.0,
                        margin: EdgeInsets.symmetric(
                          horizontal: 70,
                        ),
                        child: FittedBox(
                          child: RaisedButton(
                            onPressed: () {},
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(80.0)),
                            padding: EdgeInsets.all(0.0),
                            color: Colors.white,
                            child: Container(
                              constraints: BoxConstraints(
                                maxWidth: 300.0,
                                minHeight: 50.0,
                              ),
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(
                                  30.0,
                                ),
                              ),
                              padding: EdgeInsets.symmetric(
                                horizontal: 20,
                                vertical: 20,
                              ),
                              alignment: Alignment.center,
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "Let's talk ",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color: Colors.blue,
                                      fontSize: 20,
                                      fontWeight: FontWeight.normal,
                                    ),
                                  ),
                                  SizedBox(
                                    width: 20,
                                  ),
                                  Icon(
                                    Icons.arrow_forward,
                                    color: Colors.blue,
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  SliverToBoxAdapter(
                    child: FadeIn(
                      delay: 12,
                      duration: Duration(milliseconds: 800),
                      child: Container(
                        margin: EdgeInsets.only(
                            left: 40.0, right: 40.0, top: 100.0),
                        padding: EdgeInsets.all(15.0),
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(10.0),
                            shape: BoxShape.rectangle,
                            border: Border.all(
                                color: Colors.white.withOpacity(0.08)),
                            gradient: LinearGradient(colors: [
                              Colors.white.withOpacity(0.2),
                              Colors.white.withOpacity(0.05),
                            ])),
                        child: Container(
                          alignment: Alignment.center,
                          child: Text(
                            "We hope you enjoy our app",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 12,
                            ),
                          ),
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
