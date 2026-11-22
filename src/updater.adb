package body Updater is

   function First_Blocker
     (Newer : Boolean; Token_OK : Boolean; A : Asset_Set) return Blocker
   is
   begin
      if not Newer then
         return No_New_Version;
      end if;
      if not Token_OK then
         return Bad_Token;
      end if;
      if not A.Linux_X86_64 then
         return Missing_Linux_X86_64;
      end if;
      if not A.Linux_AArch64 then
         return Missing_Linux_AArch64;
      end if;
      if not A.Macos_DMG then
         return Missing_Macos_DMG;
      end if;
      return None;
   end First_Blocker;

end Updater;
