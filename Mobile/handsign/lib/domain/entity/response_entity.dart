class ResponseEntity {
  final String label;
  final double confidence;

  ResponseEntity({
    this.label,
    this.confidence,
  });

  @override
  bool operator ==(Object o) {
    if (identical(this, o)) return true;

    return o is ResponseEntity &&
        o.label == label &&
        o.confidence == confidence;
  }

  @override
  int get hashCode => label.hashCode ^ confidence.hashCode;

  ResponseEntity copyWith({
    String label,
    double confidence,
  }) {
    return ResponseEntity(
      label: label ?? this.label,
      confidence: confidence ?? this.confidence,
    );
  }
}
