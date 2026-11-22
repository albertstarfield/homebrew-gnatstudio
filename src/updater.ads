package Updater with SPARK_Mode => On is

   --  GNAT Studio ships Linux binaries on GitHub and the macOS DMG on
   --  SourceForge; both must be present before a release can be published.
   type Asset_Set is record
      Linux_X86_64  : Boolean;
      Linux_AArch64 : Boolean;
      Macos_DMG     : Boolean;
   end record;

   type Blocker is
     (None, No_New_Version, Bad_Token, Missing_Linux_X86_64,
      Missing_Linux_AArch64, Missing_Macos_DMG);

   function All_Assets (A : Asset_Set) return Boolean is
     (A.Linux_X86_64 and then A.Linux_AArch64 and then A.Macos_DMG);

   function Ready (Newer, Token_OK : Boolean; A : Asset_Set) return Boolean is
     (Newer and then Token_OK and then All_Assets (A));

   function First_Blocker
     (Newer : Boolean; Token_OK : Boolean; A : Asset_Set) return Blocker
   with Post =>
     (case First_Blocker'Result is
        when None     => Ready (Newer, Token_OK, A),
        when others   => not Ready (Newer, Token_OK, A));

end Updater;
