with Ada.Text_IO; use Ada.Text_IO;
with Updater;

--  I/O boundary only. The release-readiness decision is in SPARK Updater.
procedure Main with SPARK_Mode => Off is

   function Read_Bool (Key : String) return Boolean is
      Line : constant String := Get_Line;
   begin
      return Line = Key & "=1";
   end Read_Bool;

   Newer    : constant Boolean := Read_Bool ("newer");
   Token_OK : constant Boolean := Read_Bool ("token");
   A        : Updater.Asset_Set;

begin
   A.Linux_X86_64  := Read_Bool ("linux_x86_64");
   A.Linux_AArch64 := Read_Bool ("linux_aarch64");
   A.Macos_DMG     := Read_Bool ("macos_dmg");
   Put_Line (Updater.Blocker'Image (Updater.First_Blocker (Newer, Token_OK, A)));
end Main;
