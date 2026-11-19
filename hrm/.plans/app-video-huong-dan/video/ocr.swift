import Foundation
import Vision
import AppKit
// ocr <png>  → mỗi dòng: x y w h<TAB>text  (toạ độ chuẩn hoá 0..1, gốc trên-trái)
let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let img = NSImage(contentsOf: url), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { exit(1) }
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.recognitionLanguages = ["vi-VN", "en-US"]
req.usesLanguageCorrection = false
try VNImageRequestHandler(cgImage: cg).perform([req])
for o in req.results ?? [] {
  guard let t = o.topCandidates(1).first else { continue }
  let b = o.boundingBox
  print(String(format: "%.4f %.4f %.4f %.4f\t", b.minX, 1 - b.maxY, b.width, b.height) + t.string)
}
