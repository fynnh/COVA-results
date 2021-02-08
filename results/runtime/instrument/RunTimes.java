import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableKeyException;
import java.security.cert.CertificateException;
import java.util.List;

public class RunTimes {


  public static void main(String[] args) throws IOException, UnrecoverableKeyException,
      KeyStoreException, NoSuchAlgorithmException, CertificateException, InterruptedException {
    Path basePath = Paths.get("/home/fynn/Dokumente/masterarbeit/open_source_apps/error_apks2");
    PrintStream ps =
        new PrintStream(Files.newOutputStream(basePath.getParent().resolve("times.csv")));
    ps.println("filename;filesize;bodies;analyzedBodies;units;targets;time");
    try (DirectoryStream<Path> ds = Files.newDirectoryStream(basePath)) {
      for (Path dirname : ds) {
        if (!Files.isDirectory(dirname)) {
          continue;
        }
        try (DirectoryStream<Path> ds2 = Files.newDirectoryStream(dirname)) {
          for (Path p : ds2) {
            if (Files.isDirectory(p)) {
              continue;
            }
            if (p.toString().endsWith(".apk")) {
              try {


                // invoke the methods and other classes that are not allowed to call System.exit.
                System.out.println(p);
                soot.G.reset();
                long instrumentStart = System.currentTimeMillis();
                int targets = instrument(p);

                long instrumentEnd = System.currentTimeMillis();
                long diff = instrumentEnd - instrumentStart;;

                ps.println(p.getFileName().toString() + ";" + Files.size(p) + ";"
                    + SootInstrumenter.bodies + ";" + SootInstrumenter.analyzedBodies + ";"
                    + SootInstrumenter.unitsNo + ";" + targets + ";" + diff);
                System.out.println(diff);
                Files.move(dirname,
                    Paths.get("/home/fynn/Dokumente/masterarbeit/open_source_apps/ok_apks")
                        .resolve(dirname.getFileName()));



              } catch (Exception e) {
                e.printStackTrace();
                Files.move(dirname,
                    Paths.get("/home/fynn/Dokumente/masterarbeit/open_source_apps/error_apks")
                        .resolve(dirname.getFileName()));
              }
            }
          }
        }
      }
    }
  }

  static int instrument(Path apkFile) throws IOException, UnrecoverableKeyException,
      KeyStoreException, NoSuchAlgorithmException, CertificateException, InterruptedException {
    Path platformDir = Paths.get(
        "/home/fynn/Dokumente/masterarbeit/my_data/COVA/cova/src/test/resources/androidPlatforms");
    Path dir = Files.createTempDirectory("runtime");
    Path targetApk = dir.resolve("target_" + apkFile.getFileName().toString());
    Path signedApk = dir.resolve("signed_" + apkFile.getFileName().toString());
    Path alignedApk = dir.resolve("aligned_" + apkFile.getFileName().toString());
    ApkSignHelper apkSignHelper = new ApkSignHelper();
    SootInstrumenter instrumenter = new SootInstrumenter();


    // Instrument apk with logcat outputs
    List<TargetStrings> possibleTargets = instrumenter.instrument(apkFile, targetApk, platformDir);
    System.out.println("Start sign");
    // sign instrumented apk
    apkSignHelper.sign(targetApk, signedApk, alignedApk);
    System.out.println("Finish");

    return possibleTargets.size();
  }
}
